FROM python:3.11-slim

# Evita la generazione di file .pyc e forza l'output immediato dei log
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 1. Crea un gruppo e un utente non di sistema (UID/GID 1001)
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -s /bin/bash -m appuser

WORKDIR /app

# 2. Installa le dipendenze con caching ottimizzato
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia l'applicazione impostando i permessi corretti per appuser
COPY --chown=appuser:appgroup . .

# 4. Esegui il processo come utente non-root
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
