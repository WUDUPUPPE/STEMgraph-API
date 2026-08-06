# STEMgraph API

Die STEMgraph API ist der Backend-Teil des STEMgraph-Projekts. Sie stellt eine REST-Schnittstelle bereit, über die Challenge-Daten, Graph-Strukturen und Abhängigkeitsbeziehungen aus einer Neo4j-Datenbank abgefragt werden können. Ziel ist es, die Datenbank nicht direkt vom Frontend aus anzusprechen, sondern über ein klar definiertes Backend zu kapseln.

Die API wurde mit FastAPI in Python umgesetzt und ist so aufgebaut, dass sie in Docker-Containern betrieben und mit Docker Compose zusammen mit Neo4j gestartet werden kann. Dadurch entsteht eine reproduzierbare, saubere und erweiterbare Projektstruktur.

## Projektziel

Das Ziel der STEMgraph API ist es, die im Projekt gesammelten Challenge-Daten zentral bereitzustellen und den Zugriff darauf zu vereinheitlichen. Statt dass das Frontend direkt auf Neo4j zugreift, übernimmt die API die Kommunikation mit der Datenbank und gibt die Informationen in strukturierter Form zurück.

Dadurch werden mehrere Vorteile erreicht:

- Die Datenbank bleibt hinter dem Backend verborgen.
- Das Frontend wird einfacher, da es nur HTTP-Anfragen senden muss.
- Die Logik für Datenzugriff und Datenaufbereitung liegt an einer zentralen Stelle.
- Die Architektur wird wartbarer und besser erweiterbar.

## Architektur

Die Anwendung besteht aus drei Hauptbestandteilen:

1. **FastAPI-Anwendung**
   - nimmt Anfragen entgegen
   - verarbeitet Parameter
   - führt Datenbankabfragen aus
   - gibt JSON-Antworten zurück

2. **Neo4j-Datenbank**
   - speichert Challenges als Knoten
   - speichert Abhängigkeiten als Beziehungen
   - bildet den Graphen für das Projekt

3. **Docker-Umgebung**
   - startet die Anwendung reproduzierbar
   - kapselt API und Datenbank
   - erleichtert Deployment und Entwicklung

Die API kommuniziert mit Neo4j über den Bolt-Zugriff. Im Docker-Setup wird dafür das interne Docker-Netzwerk verwendet, sodass die Datenbank nicht direkt nach außen geöffnet werden muss.

## Verwendete Technologien

- Python
- FastAPI
- Uvicorn
- Neo4j
- Cypher
- Pydantic
- Docker
- Docker Compose

## Funktionsweise

Die API nimmt HTTP-Anfragen entgegen und verarbeitet sie in den passenden Endpoints. Je nach Anforderung werden Cypher-Abfragen an Neo4j gesendet, die Ergebnisse ausgelesen und anschließend als JSON strukturiert zurückgegeben.

Die Response-Modelle sorgen dafür, dass die Daten in einem einheitlichen Format ausgegeben werden. Das ist besonders wichtig, damit das Frontend zuverlässig mit den Antworten arbeiten kann.

Typische Aufgaben der API sind:

- vollständige Listen von Challenges bereitstellen
- Beziehungen zwischen Challenges auslesen
- Pfade im Graphen ermitteln
- Nachbarn oder direkte Vorgänger/Nachfolger zurückgeben
- Graphdaten in einer für das Frontend nutzbaren Form liefern

## Datenmodell

Die Daten in Neo4j werden als Graph gespeichert. Dabei entsprechen die Challenges Knoten und die Abhängigkeiten zwischen ihnen den Beziehungen.

Typische Eigenschaften eines Challenge-Knotens sind:

- `id`
- `teaches`
- `keywords`
- `author`
- `firstused`

Die Beziehungen beschreiben, wie einzelne Challenges voneinander abhängen. Dadurch kann die API nicht nur einzelne Datensätze ausgeben, sondern auch Lernpfade und Graphzusammenhänge darstellen.

## Endpoints

Die API ist so aufgebaut, dass sie mehrere fachlich getrennte Endpoints bereitstellt. Beispiele für geplante oder bereits vorgesehene Funktionen sind:

- `GET /get_graph` or `GET /get_list`
- `GET /get_subgraph`
- `GET /get_keywords_graph` or `GET /get_keywords_list`
- `GET /get_challenges_by_keyword_graphh`
- `GET /get_list_dependencies`
- `POST /admin_update_challenges`
- weitere Graph-, List- und Nachbarschaftsabfragen
- Detailabfragen für einzelne Challenges
- Ausgaben für Popup-Ansichten im Frontend

Wichtig ist dabei nicht nur, dass Daten ausgegeben werden, sondern dass sie direkt in der passenden Struktur für das Frontend bereitstehen.

### Beispielhafte Aufgaben der Endpoints

- alle vorhandenen Challenges auflisten
- einen Pfad zwischen zwei Knoten ermitteln
- direkte Nachbarn einer Challenge anzeigen
- Graphdaten für die visuelle Darstellung liefern
- Abhängigkeiten für Lernpfade berechnen

## Beispiel-Requests

### Alle Challenges abrufen

```http
GET /get_list
```

Beispiel für eine mögliche Antwort:

```json
{
  "items": [
    {
      "id": "challenge-1",
      "teaches": "Basics",
      "keywords": ["python", "data"],
      "author": "Example Author",
      "firstused": "2025-04-07"
    }
  ]
}
```

### Graphdaten abrufen

```http
GET /get_graph
```

Beispiel für eine mögliche Antwort:

```json
{
  "nodes": [
    {
      "id": "challenge-1",
      "label": "challenge-1"
    }
  ],
  "edges": [
    {
      "source": "challenge-1",
      "target": "challenge-2",
      "type": "DEPENDS_ON"
    }
  ]
}
```

### Pfad zwischen zwei Knoten abrufen

```http
GET /get_subgraph?from=challenge-1&to=challenge-5
```

Beispiel für eine mögliche Antwort:

```json
{
  "path": [
    "challenge-1",
    "challenge-2",
    "challenge-5"
  ]
}
```

## Response-Struktur

Die API liefert die Antworten als JSON zurück. Dadurch kann das Frontend die Daten direkt weiterverarbeiten, ohne selbst aufwendig mit der Datenbank kommunizieren zu müssen.

Ein einheitliches Antwortformat ist wichtig, weil:

- Daten besser nachvollziehbar sind
- Fehlersuche einfacher wird
- das Frontend stabiler mit der API arbeiten kann
- Erweiterungen leichter ergänzt werden können

## Installation

### Voraussetzungen

- Python 3.11 oder neuer
- Docker
- Docker Compose
- Zugriff auf eine Neo4j-Datenbank

### Lokaler Start

Wenn die Anwendung lokal entwickelt wird, kann sie über eine virtuelle Umgebung gestartet werden:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Start mit Docker

Die komplette Anwendung kann auch über Docker Compose gestartet werden:

```bash
docker compose up --build
```

## Konfiguration

Falls Umgebungsvariablen genutzt werden, können sie zum Beispiel so aussehen:

```env
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PW=example
```

## Docker-Setup

Die STEMgraph API ist für den Betrieb in Docker vorgesehen. Das heißt, sowohl die FastAPI-Anwendung als auch Neo4j können als Container gestartet werden.

Der Vorteil daran ist:

- reproduzierbare Umgebung
- saubere Trennung der Dienste
- einfacher Start per Docker Compose
- bessere Nachvollziehbarkeit für Entwicklung und Deployment

## Lokale Entwicklung

Für die Entwicklung kann die API lokal in einer Python-Umgebung gestartet werden. In diesem Fall werden die Abhängigkeiten in einer virtuellen Umgebung installiert und der Server über Uvicorn gestartet.

Typischer Ablauf:

1. virtuelle Umgebung anlegen
2. Abhängigkeiten installieren
3. API konfigurieren
4. FastAPI-Server starten
5. Endpoints testen

Das erleichtert das Debugging und die schrittweise Entwicklung neuer Funktionen.

## Erweiterungsmöglichkeiten

Die Architektur ist so gedacht, dass sie später ausgebaut werden kann. Mögliche Erweiterungen sind:

- zusätzliche Endpoints
- Filterfunktionen
- Authentifizierung mit Keycloak
- rollenbasierte Zugriffe
- erweiterte Graphanalysen
- weitere Export- und Importfunktionen

Gerade die spätere Authentifizierungsschicht macht die Trennung zwischen Frontend, API und Datenbank noch wichtiger.

## Projektstand

Der aktuelle Projektstand umfasst eine fertige REST-basierte Architektur für den praktischen Einsatz im Projekt. Die API dient bereits als zentraler Zugangspunkt zwischen Frontend und Neo4j und erfüllt die dafür vorgesehenen Aufgaben im laufenden Entwicklungsumfeld.

Im nächsten Schritt steht vor allem das Deployment auf einem echten Server bzw. in einer produktionsnahen Umgebung im Vordergrund. Dabei geht es darum, die bestehende Anwendung stabil bereitzustellen und die Verbindung zur Datenbank in der finalen Umgebung sauber zu betreiben.

## Fazit

Die STEMgraph API bildet die Grundlage für eine strukturierte und wartbare Backend-Architektur. Sie trennt die Datenhaltung von der Darstellung, macht den Zugriff auf Graphdaten einheitlich und schafft eine saubere Grundlage für den weiteren Betrieb und spätere Erweiterungen.

Damit ist die API nicht nur ein technischer Zwischenschritt, sondern ein zentraler Baustein für die weitere Entwicklung des Projekts.
