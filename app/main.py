import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import bets, ingest, stats

app_name = os.getenv("APP_NAME", "CALEBet API")
app_version = os.getenv("APP_VERSION", "1.0.0")

app = FastAPI(
    title=app_name,
    description="API do sistema CALEBet (Central de Análises e Estatísticas de Apostas Esportivas).",
    version=app_version,
    contact={
        "name": "Equipe CALEBet",
        "url": "https://calebet.app",
        "email": "dev@calebet.app",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

origins = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bets.router, tags=["Bets"])
app.include_router(ingest.router, tags=["Ingestão"])
app.include_router(stats.router)


@app.get("/")
def root():
    return {"message": "CALEBet backend up"}


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok", "service": app_name}


print("Swagger disponível em http://localhost:8000/docs")
