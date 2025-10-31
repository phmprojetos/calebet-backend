"""Database models for bets."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Numeric, String

from app.db import Base


class Bet(Base):
    """Represents a bet registered in the system."""

    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    event = Column(String(255), nullable=False)
    market = Column(String(255), nullable=False)
    selection = Column(String(255), nullable=False)
    odds = Column(Numeric(10, 2), nullable=False)
    stake = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
