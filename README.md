# Vulnerable Lab

Repository di esempio per il laboratorio didattico "Vulnerable Lab".

Questo repository contiene scenari vulnerabili containerizzati per finalità didattiche.

Esempi inclusi:
- `sql-injection` (esempio minimo funzionante)
- `broken-auth` (scaffold)
- `privilege-escalation` (scaffold)
- `misconfiguration` (scaffold)

Esecuzione (esempio):

```bash
cd VulnerableLab
docker-compose up --build
# aprire http://localhost:5000/init per inizializzare il DB
# aprire http://localhost:5000/search?q=alice per provare la ricerca
```

Nota: questo repository è pensato per essere linkato dalla tesi; mantieni il codice separato dalla parte LaTeX.
