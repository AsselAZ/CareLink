from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models


from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router
from app.api.ratings import router as ratings_router
from app.api.notifications import router as notifications_router
from app.api.messages import router as messages_router

# Erstellt unsere FastApi Anwendung.
# Über dieses Objekt werden später alle Api Routen erreichbar sein

app = FastAPI(
    title="CareLink API"
)

# Fügt CORS-Middleware hinzu, um Cross-Origin-Requests zu erlauben. also locla : 3000 undd local : 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    # get and post requests are allowed put and delete are not allowed
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(ratings_router)
app.include_router(notifications_router)
app.include_router(messages_router)