from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import bets, ingest, stats


app = FastAPI(
    title="CALEBet API",
    description="API do sistema CALEBet (Central de Análises e Estatísticas de Apostas Esportivas).",
    version="1.0.0",
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {"status": "ok"}


print("✅ Swagger disponível em http://localhost:8000/docs")
