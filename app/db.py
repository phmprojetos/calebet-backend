import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)


if os.getenv("APP_ENV") != "production":
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)


supabase_database_url = os.getenv("SUPABASE_DATABASE_URL")
database_url = supabase_database_url or os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("❌ DATABASE_URL não encontrada. Verifique o .env e as variáveis de ambiente.")

if supabase_database_url:
    logger.info("✅ Using SUPABASE_DATABASE_URL (likely Supabase Pooler).")
else:
    logger.info("⚠️ Using DATABASE_URL fallback (Render internal or .env).")

try:
    parsed_url = make_url(database_url)
    host = parsed_url.host or "unknown"
    port = parsed_url.port or "default"
    logger.info("🔍 Database target: host=%s port=%s", host, port)
except Exception as exc:  # pragma: no cover - parsing failure should not break startup
    logger.debug("Could not parse database URL for host/port details: %s", exc)


engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
