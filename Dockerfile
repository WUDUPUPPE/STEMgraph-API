FROM python:3.12-slim

# Cron installieren
RUN apt-get update && apt-get install -y cron

# App kopieren
COPY . /app
WORKDIR /app

# Cronjob einrichten
COPY cronjob /etc/cron.d/stemgraph
RUN chmod 0644 /etc/cron.d/stemgraph

# Cron und FastAPI starten
CMD cron && uvicorn app.main:app --host 0.0.0.0 --port 8000