FROM python:3.11-slim

# Evita file .pyc e forza flushing immediato dei log
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 1. Crea un gruppo e utente non privilegiati (UID/GID 1001)
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -s /bin/bash -m appuser

WORKDIR /app

# 2. Caching dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia il codice impostando appuser come proprietario
COPY --chown=appuser:appgroup . .

# 4. Esegui il processo come utente non-root
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
