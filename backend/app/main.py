from fastapi import FastAPI

import app.models

from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router

# Erstellt unsere FastApi Anwendung.
# Über dieses Objekt werden später alle Api Routen erreichbar sein

app = FastAPI(
    title="CareLink API"
)

# Ein einfacher Test Endpunkt zu prüfen,
# ob das Backend korrekt gestartet wurde.
@app.get("/")
def root():
    return {"message": "CareLink API läuft"}

# User-Routen mit der Hauptanwendung verbinden
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(tasks_router)

