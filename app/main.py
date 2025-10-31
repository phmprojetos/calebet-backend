from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import bets as bets_api
from app.api import ingest as ingest_api
from app.db import Base, engine


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


app = FastAPI(title="Calebet Backend")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    create_tables()


app.include_router(bets_api.router)
app.include_router(ingest_api.router)


@app.get("/", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
