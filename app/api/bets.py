"""API endpoints for managing bets."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import BetCreate, BetRead
from app.services import BetsService

router = APIRouter(prefix="/bets", tags=["bets"])


@router.get("/", response_model=List[BetRead])
def list_bets(db: Session = Depends(get_db)) -> List[BetRead]:
    """Retrieve all registered bets."""
    bets = BetsService.list_bets(db)
    return list(bets)


@router.post("/", response_model=BetRead, status_code=status.HTTP_201_CREATED)
def create_bet(bet_in: BetCreate, db: Session = Depends(get_db)) -> BetRead:
    """Create a new bet record."""
    try:
        return BetsService.create_bet(db, bet_in)
    except Exception as exc:  # pragma: no cover - simple example handling
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
