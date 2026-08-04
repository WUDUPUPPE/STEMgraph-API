FROM python:3.13-slim

#Installiert curl und entfernt den Cache, um das Image klein zu halten
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

#Installiert cron und entfernt den Cache, um das Image klein zu halten
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

#Setzt das Arbeitsverzeichnis auf /app
WORKDIR /app

#Kopiert die requirements.txt Datei in das Arbeitsverzeichnis und installiert die Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Kopiert den Rest des Codes in das Arbeitsverzeichnis
COPY . .

#Kopiert die cronjob Datei in das Verzeichnis /etc/cron.d und setzt die Berechtigungen
COPY cronjob /etc/cron.d/stemgraph
RUN chmod 0644 /etc/cron.d/stemgraph

#Fügt den cronjob zur crontab hinzu
RUN touch /var/log/cron.log

#Startet die FastAPI Anwendung
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]