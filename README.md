# Vulnerable Lab

Repository di esempio per il laboratorio didattico "Vulnerable Lab".

Il progetto contiene scenari vulnerabili containerizzati per finalita' didattiche. Gli scenari sono intenzionalmente insicuri e devono essere eseguiti solo in ambiente locale e controllato.

Scenari inclusi:
- `sql-injection`
- `broken-auth`
- `privilege-escalation`
- `misconfiguration`

## Avvio

```bash
cd VulnerableLab
docker compose up -d --build
```

Il comando usa la sintassi di Docker Compose v2 (`docker compose`), integrata nella CLI di Docker. Il file di configurazione mantiene il nome convenzionale `docker-compose.yml`.

Endpoint principali:
- SQL Injection: `http://localhost:5000/init` e `http://localhost:5000/search?q=alice`
- Broken Authentication: `http://localhost:5001/login`
- Accesso improprio a risorsa privilegiata: `http://localhost:5002/read-secret`
- Misconfiguration: `http://localhost:5003/admin`

## Verifica automatica di base

La cartella `scripts` contiene uno script PowerShell che esegue una verifica automatica minima del laboratorio:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test-lab.ps1
```

Lo script:
- avvia il laboratorio con `docker compose up -d --build`, salvo uso di `-SkipStart`;
- verifica che Docker e Docker Compose siano disponibili;
- controlla che i quattro servizi siano raggiungibili;
- valida gli endpoint principali degli scenari vulnerabili;
- verifica che ogni container sia collegato alla propria rete dedicata.

Se il laboratorio e' gia' avviato:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test-lab.ps1 -SkipStart
```

## Arresto

```bash
docker compose down
```

Nota: questo repository e' pensato per essere linkato dalla tesi; mantieni il codice separato dalla parte LaTeX.
