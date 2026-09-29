FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 1. Crea utente e gruppo dedicati
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -s /bin/bash -m appuser

# 2. Il segreto appartiene a root con permessi restrittivi (chmod 600: solo root può leggerlo)
RUN mkdir -p /root && \
    echo "TOP_SECRET=DoNotExpose" > /root/secret.txt && \
    chmod 600 /root/secret.txt && \
    chmod 700 /root

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup . .

# 3. L'applicazione gira come appuser (non-root)
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
