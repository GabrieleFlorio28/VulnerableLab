param(
    [switch]$SkipStart,
    [int]$TimeoutSeconds = 45
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$LabRoot = Split-Path -Parent $PSScriptRoot
Set-Location $LabRoot

function Write-Pass {
    param([string]$Message)
    Write-Host "[PASS] $Message" -ForegroundColor Green
}

function Write-Step {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Assert-True {
    param(
        [string]$Name,
        [bool]$Condition,
        [string]$FailureMessage
    )

    if (-not $Condition) {
        throw "[FAIL] $Name - $FailureMessage"
    }

    Write-Pass $Name
}

function Invoke-LabRequest {
    param(
        [string]$Name,
        [string]$Uri,
        [string]$ExpectedText,
        [string]$Method = "GET",
        [hashtable]$Body = $null
    )

    if ($Method -eq "POST") {
        $response = Invoke-WebRequest -Uri $Uri -Method Post -Body $Body -ContentType "application/x-www-form-urlencoded" -UseBasicParsing -TimeoutSec 10
    } else {
        $response = Invoke-WebRequest -Uri $Uri -UseBasicParsing -TimeoutSec 10
    }

    Assert-True $Name ($response.Content.Contains($ExpectedText)) "expected text not found: $ExpectedText"
}

function Wait-ForHttp {
    param(
        [string]$Name,
        [string]$Uri
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            Invoke-WebRequest -Uri $Uri -UseBasicParsing -TimeoutSec 5 | Out-Null
            Write-Pass "$Name reachable"
            return
        } catch {
            Start-Sleep -Seconds 2
        }
    }

    throw "[FAIL] $Name reachable - service did not answer within $TimeoutSeconds seconds"
}

Write-Step "Checking Docker availability"
docker --version | Out-Null
docker compose version | Out-Null
Write-Pass "Docker and Docker Compose available"

if (-not $SkipStart) {
    Write-Step "Building and starting the lab"
    docker compose up -d --build
    Write-Pass "Docker Compose startup completed"
}

$services = @(
    @{ Name = "sql-injection"; Port = 5000; NetworkSuffix = "_sql_net" },
    @{ Name = "broken-auth"; Port = 5001; NetworkSuffix = "_auth_net" },
    @{ Name = "privilege-escalation"; Port = 5002; NetworkSuffix = "_priv_net" },
    @{ Name = "misconfiguration"; Port = 5003; NetworkSuffix = "_misconf_net" }
)

Write-Step "Checking service availability"
foreach ($service in $services) {
    Wait-ForHttp $service.Name "http://localhost:$($service.Port)/"
}

Write-Step "Checking running containers"
$runningServices = @(docker compose ps --services --status running)
foreach ($service in $services) {
    Assert-True "container running: $($service.Name)" ($runningServices -contains $service.Name) "service is not listed as running"
}

Write-Step "Checking vulnerable scenario responses"
Invoke-LabRequest "SQL database initialization" "http://localhost:5000/init" "SQLite database initialized"
Invoke-LabRequest "SQL normal search" "http://localhost:5000/search?q=alice" "alice"
Invoke-LabRequest "SQL injection observable output" "http://localhost:5000/search?q=%27%20OR%20%271%27%3D%271" "admin"
Invoke-LabRequest "Broken Authentication weak login" "http://localhost:5001/login" "Logged in as alice" "POST" @{ username = "alice"; password = "pas" }
Invoke-LabRequest "Privileged resource exposure" "http://localhost:5002/read-secret" "TOP_SECRET=DoNotExpose"
Invoke-LabRequest "Misconfiguration admin endpoint" "http://localhost:5003/admin" "Admin panel"

Write-Step "Checking one-network-per-scenario isolation"
foreach ($service in $services) {
    $containerId = (docker compose ps -q $service.Name).Trim()
    Assert-True "container id available: $($service.Name)" ($containerId.Length -gt 0) "docker compose did not return a container id"

    $inspect = docker inspect $containerId | ConvertFrom-Json
    $networkNames = @($inspect[0].NetworkSettings.Networks.PSObject.Properties | ForEach-Object { $_.Name })
    $matchingNetworks = @($networkNames | Where-Object { $_.EndsWith($service.NetworkSuffix) })
    $hasExpectedNetwork = $matchingNetworks.Count -eq 1

    Assert-True "single network attachment: $($service.Name)" ($networkNames.Count -eq 1) "found networks: $($networkNames -join ', ')"
    Assert-True "expected network for $($service.Name)" $hasExpectedNetwork "expected suffix $($service.NetworkSuffix), found: $($networkNames -join ', ')"
}

Write-Host ""
Write-Host "All Vulnerable Lab checks completed successfully." -ForegroundColor Green
