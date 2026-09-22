FROM python:3.11-slim

# Crea un utente di sistema non-root dedicato
RUN useradd -m -u 1001 appuser

WORKDIR /app

# Copia i requisiti e installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice assegnando la proprietà dei file all'utente non privilegiato
COPY --chown=appuser:appuser . .

# Passa all'utente non-root prima dell'esecuzione
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
