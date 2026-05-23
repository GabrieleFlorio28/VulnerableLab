FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# create a root-owned secret file to demonstrate privilege exposure
RUN mkdir -p /root && echo "TOP_SECRET=DoNotExpose" > /root/secret.txt && chmod 644 /root/secret.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
