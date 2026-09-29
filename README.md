# Remediated Lab (Hardened)

Repository di esempio per il laboratorio didattico "Remediated Lab".

Il progetto contiene gli scenari containerizzati del laboratorio "Vulnerable Lab" dopo l'applicazione delle contromisure di sicurezza (remediation) a livello di codice applicativo, configurazione dei container e policy DevSecOps.

Scenari mitigati inclusi:
- `sql-injection`: Adozione di prepared statements e query parametrizzate contro injection SQL.
- `broken-auth`: Hashing crittografico delle password (PBKDF2/SHA256) con verifica a tempo costante e normalizzazione degli errori contro l'enumerazione account.
- `privilege-escalation`: Esecuzione su container non-root (`USER appuser`), hardening dei permessi POSIX (`chmod 600`), revoca delle capability kernel (`cap_drop: ALL`) e flag `no-new-privileges: true`.
- `misconfiguration`: Disattivazione della modalità debug a runtime, blocco delle rotte riservate (`403 Forbidden`) e iniezione di Security Headers HTTP difensivi.

## Avvio

```bash
cd RemediatedLab
docker compose up -d --build
```

Il comando usa la sintassi di Docker Compose v2 (`docker compose`), integrata nella CLI di Docker. Il file di configurazione mantiene il nome convenzionale `docker-compose.yml`.

Endpoint principali:
- SQL Injection (Mitigato): http://localhost:5000/init e http://localhost:5000/search?q=alice
- Authentication (Sicura): http://localhost:5001/login
- Risorsa protetta (Access Control): http://localhost:5002/read-secret
- Misconfiguration (Hardened): http://localhost:5003/admin
## Verifica automatica di base

La cartella `scripts` contiene uno script PowerShell che esegue una verifica automatica minima del laboratorio:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test-lab.ps1
```

Lo script:
- avvia il laboratorio con `docker compose up -d --build`, salvo uso di `-SkipStart`;
- verifica che Docker e Docker Compose siano disponibili;
- controlla che i quattro servizi siano raggiungibili;
- valida l'efficacia delle mitigazioni (es. rifiuto di payload malevoli, risposte di errore neutre, accesso non privilegiato);
- verifica che ogni container sia collegato alla propria rete dedicata.

Se il laboratorio e' gia' avviato:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test-lab.ps1 -SkipStart
```

- `.github/workflows/`: Pipeline CI/CD di security scanning automatizzato (Gitleaks, pip-audit, Trivy).

## Arresto

```bash
docker compose down
```

Nota: questo repository e' pensato per essere linkato dalla tesi; mantieni il codice separato dalla parte LaTeX.
