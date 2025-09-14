# Basis-Image mit Python
FROM python:3.11-slim

# Arbeitsverzeichnis
WORKDIR /app

# Dependencies installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Datei kopieren
COPY app.py .

# Container-Startbefehl
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]