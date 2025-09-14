Perfekt 👍 Hier ist dein Dockerfile-Spickzettel als Markdown – kannst du direkt in deine Doku oder doc/-Ordner packen:

# 📝 Dockerfile Spickzettel

## Basis & Struktur
```dockerfile
FROM <image>[:tag]

➡️ Startpunkt festlegen (z. B. python:3.11-slim, ubuntu:22.04).

WORKDIR /pfad

➡️ Arbeitsverzeichnis im Container setzen (ähnlich wie cd).

COPY <src> <dest>

➡️ Dateien vom Host ins Image kopieren.
Beispiel: COPY app.py /app/

ADD <src> <dest>

➡️ Wie COPY, kann zusätzlich Archive entpacken oder URLs laden.
👉 In der Praxis fast immer COPY besser.

## Pakete & Installation
```dockerfile
RUN <befehl>

➡️ Führt einen Befehl während des Image-Builds aus.
Beispiel: RUN apt-get update && apt-get install -y curl

ENV NAME=wert

➡️ Umgebungsvariablen setzen (z. B. für Config).

⸻

Start & Ausführung

CMD ["programm", "arg1", "arg2"]

➡️ Standardstartbefehl beim Container-Start.
👉 Nur eine CMD pro Dockerfile (falls mehrere → nur letzte zählt).

ENTRYPOINT ["programm"]

➡️ Wie CMD, aber „fester“ → man kann beim docker run zusätzliche Parameter anhängen.
Beispiel: ENTRYPOINT ["python"] + docker run image app.py

EXPOSE 8000

➡️ Dokumentiert, dass der Container Port 8000 verwendet.
(keine echte Firewall-Funktion, rein Info für Tools wie Docker Compose/K8s).

⸻

Caching & Optimierung
	•	Befehle in logische Blöcke packen (z. B. erst requirements.txt kopieren, dann installieren).
	•	Reihenfolge ist wichtig → Docker cached jede Schicht.
	•	Kleine Basis-Images verwenden (z. B. python:3.11-slim statt python:3.11).

⸻

🚀 Mini-Beispiel (Python FastAPI Service)

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

---

👉 Soll ich dir diesen Spickzettel gleich als **fertige Datei `doc/dockerfile_cheatsheet.md`** vorbereiten, damit du ihn direkt in dein Projekt einchecken kannst?