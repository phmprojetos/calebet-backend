import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# === Carrega o .env ===
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL não encontrada. Verifique o .env e o caminho.")

print(f"Loaded DATABASE_URL (partial): {DATABASE_URL[:60]}...")

# === Cria Engine e Session ===
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Exporta Base
Base = declarative_base()

# === Função get_db ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
