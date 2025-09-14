# Ziel

Ziel: Mit dieser Anleitung kannst du den „Health-Service“ als FastAPI-Anwendung in Docker jederzeit von Grund auf neu aufsetzen, beliebig viele Instanzen starten und per Health-Check individuell prüfen. Die Anleitung ist Schritt für Schritt aufgebaut und funktioniert für Einsteiger wie Fortgeschrittene.

# Kompakte Checkliste für mini „Health-Service“-Dockerchen

Wenn dein Python-Code fertig ist, brauchst du nur das hier:


## Schritt 1: Projektstruktur anlegen

Lege einen neuen Ordner (z.B. `health_service/`) an und erstelle darin folgende Dateien:

```
health_service/
├─ app.py
├─ requirements.txt
├─ Dockerfile
└─ .dockerignore
```

## Schritt 2: Dateien erstellen und befüllen

**Welche Datei? Was kommt rein?**

- **app.py**: Enthält die FastAPI-App mit eindeutiger Health-Route.
- **requirements.txt**: Listet alle Python-Abhängigkeiten.
- **Dockerfile**: Beschreibt, wie das Docker-Image gebaut wird.
- **.dockerignore**: Sorgt dafür, dass unnötige Dateien nicht ins Image gelangen.

### Beispielinhalte:

**app.py**

```python
import socket
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/health")
def health():
    # Hostname oder Container-ID zur eindeutigen Identifikation ausgeben
    return JSONResponse(content={
        "status": "ok",
        "host": socket.gethostname()
    })
```

**requirements.txt**

```
fastapi
uvicorn
```

**Dockerfile**

```dockerfile
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**.dockerignore**

```
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.git
.gitignore
.vscode
.DS_Store
```

---

## Schritt 3: Image bauen

Im Projektordner ausführen:

```bash
docker build -t health-service .
```

**Hinweis:** Wenn du Änderungen an Python-Code oder Abhängigkeiten vornimmst, baue das Image erneut!

---

## Schritt 4: Einen Container starten

```bash
docker run -d -p 8000:8000 --name health health-service
```

**Testen:**

```bash
curl http://localhost:8000/health
```

Antwort:

```json
{"status":"ok","host":"<container-id oder hostname>"}
```

**Logs anzeigen (optional):**

```bash
docker logs -f health
```

**Aufräumen:**

```bash
docker stop health && docker rm health
```

---

## Schritt 5: Mehrere Container gleichzeitig starten

Du kannst beliebig viele Instanzen starten – jeder Container liefert bei `/health` eine eigene Host-ID zurück.

**Wichtig:** Vorher Image ggf. neu bauen, falls du Python-Code geändert hast!

```bash
docker build -t health-service .  # Falls nötig, erneut bauen!
```

**Beispiel: Drei Container starten (jeweils auf anderem Port):**

```bash
docker run -d -p 8001:8000 --name health1 health-service
docker run -d -p 8002:8000 --name health2 health-service
docker run -d -p 8003:8000 --name health3 health-service
```

**Testen:**

```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

Jede Antwort enthält unter `"host"` die eindeutige Container-ID.

---

## Schritt 6: Mit Docker Compose mehrere Instanzen (replicas) starten

Lege eine Datei `compose.yml` an:

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    deploy:
      replicas: 3
```

**Hinweis:** Das Feld `deploy.replicas` funktioniert mit Docker Swarm (`docker stack deploy`). Für lokales Compose (ohne Swarm) kannst du mehrere Services mit unterschiedlichen Ports definieren oder Compose v2 mit `scale` nutzen:

```bash
docker compose up --build -d --scale api=3
```

**Zugriff auf die einzelnen Instanzen:** Wenn mehrere Container denselben Port mappen, wird nur einer erreichbar sein. Am besten Ports explizit zuweisen oder Swarm nutzen. Alternativ, teste die Health-Route innerhalb des Netzwerks:

```bash
docker compose exec api curl http://localhost:8000/health
```

**Ergebnis:** Jeder Container gibt bei `/health` seine eigene Host-ID zurück:

```json
{"status":"ok","host":"eindeutige-container-id"}
```

---

## Typische Stolpersteine

- **Port belegt:** Ändere `-p 8000:8000` auf einen freien Port (z.B. `-p 8080:8000`).
- **Apple Silicon:** Das Base-Image läuft nativ auf ARM, keine Extra-Option nötig.
- **Abhängigkeiten:** Wenn du neue Pakete ergänzt, aktualisiere `requirements.txt` und baue das Image neu.

