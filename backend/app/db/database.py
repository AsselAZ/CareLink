import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Lädt die Werte aus der .env-Datei
load_dotenv()

# Datenbank-Adresse aus der .env-Datei holen
DATABASE_URL = os.getenv("DATABASE_URL")

# Stellt die Verbindung zu PostgreSQL her
engine = create_engine(DATABASE_URL)

# Erstellt Datenbank-Sessions für spätere Abfragen
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Grundlage für unsere späteren Datenbankmodelle
class Base(DeclarativeBase):
    pass

# Stellt einer Anfrage eine Datenbank-Session zur Verfügung
# und schließt sie danach wieder.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()