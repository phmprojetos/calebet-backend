import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

# Força usar o pooler do Supabase
if DATABASE_URL and "supabase.co" in DATABASE_URL and ":6543" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace(":5432", ":6543")

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
