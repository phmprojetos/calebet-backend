"""API routers for Calebet."""

from app.api.bets import router as bets_router
from app.api.ingest import router as ingest_router

__all__ = ["bets_router", "ingest_router"]
