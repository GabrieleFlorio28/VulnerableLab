FROM python:3.11-slim

# Evita la generazione di file .pyc e forza il flushing dell'output per i log del container
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Crea un utente e gruppo dedicati non privilegiati
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -s /bin/bash -m appuser

WORKDIR /app

# Copia solo le dipendenze per sfruttare il caching dei layer di Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice impostando i permessi sull'utente non-root
COPY --chown=appuser:appgroup . .

# Passa all'utente non privilegiato
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
