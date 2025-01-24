from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# SQLite-Datenbank-Konfiguration
DB_URL = "sqlite:///./stellenanzeigen.db"

# Engine und Session einrichten
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initialisiert die SQLite-Datenbank und erstellt alle Tabellen, falls sie nicht existieren.
    """
    print("Initialisiere die SQLite-Datenbank...")
    Base.metadata.create_all(bind=engine)
    print("Datenbank initialisiert.")


def get_db():
    """
    Liefert eine Session zur Interaktion mit der Datenbank.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
