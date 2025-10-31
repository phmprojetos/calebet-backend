from __future__ import annotations

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class BetResult(str, enum.Enum):
    pending = "pending"
    win = "win"
    loss = "loss"
    void = "void"
    cashout = "cashout"


class Bet(Base):
    __tablename__ = "bets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    event = Column(String)
    market = Column(String)
    odd = Column(Float)
    stake = Column(Float)
    payout_value = Column(Float, nullable=True)
    profit = Column(Float, nullable=True)
    result = Column(Enum(BetResult), default=BetResult.pending)
    is_live = Column(Boolean, default=False)
    source = Column(String)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
