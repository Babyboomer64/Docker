import socket
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
hostname = socket.gethostname()  # eindeutiger Name des Containers

@app.get("/health")
def health():
    return JSONResponse(content={
        "status": "Super-OK",
        "host": hostname
    })