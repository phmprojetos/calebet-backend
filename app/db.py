import os
from urllib.parse import quote, urlparse, urlunparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# === Lê variável única do Render ===
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# === Corrige porta do Supabase pooler ===
if "supabase.co" in DATABASE_URL and ":6543" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace(":5432", ":6543")

# === Escapa caracteres especiais da senha (ex: #, @, :, /) ===
parsed = urlparse(DATABASE_URL)
username = parsed.username or ""
hostname = parsed.hostname or ""
port = parsed.port
safe_password = quote(parsed.password or "")

if username:
    auth = f"{username}:{safe_password}" if parsed.password is not None else username
elif parsed.password is not None:
    auth = f":{safe_password}"
else:
    auth = ""

if hostname:
    host = f"{hostname}:{port}" if port else hostname
else:
    host = ""

if auth and host:
    netloc = f"{auth}@{host}"
elif host:
    netloc = host
elif auth:
    netloc = auth
else:
    netloc = parsed.netloc

DATABASE_URL = urlunparse((
    parsed.scheme,
    netloc,
    parsed.path,
    "",
    "",
    "",
))

# === Cria engine e sessão ===
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
