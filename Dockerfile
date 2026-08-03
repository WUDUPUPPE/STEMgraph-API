FROM python:3.12-slim

# Cron installieren
RUN apt-get update && apt-get install -y cron

# Arbeitsverzeichnis
WORKDIR /app

# Requirements installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App kopieren
COPY . .

# Cronjob einrichten
COPY cronjob /etc/cron.d/stemgraph
RUN chmod 0644 /etc/cron.d/stemgraph

# Log-Datei für Cronjob erstellen
RUN touch /var/log/cron.log

# Cron und FastAPI starten
CMD cron && uvicorn app.main:app --host 0.0.0.0 --port 8000