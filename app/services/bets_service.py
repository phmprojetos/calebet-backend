"""Service layer for handling bet logic."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy.orm import Session

from app.models import Bet
from app.schemas import BetCreate


class BetsService:
    """Encapsulates bet-related business logic."""

    @staticmethod
    def list_bets(db: Session) -> Iterable[Bet]:
        """Return all bets stored in the database."""
        return db.query(Bet).order_by(Bet.created_at.desc()).all()

    @staticmethod
    def create_bet(db: Session, bet_in: BetCreate) -> Bet:
        """Create a new bet entry in the database."""
        bet = Bet(**bet_in.dict())
        db.add(bet)
        db.commit()
        db.refresh(bet)
        return bet
