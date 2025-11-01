from __future__ import annotations

import enum
import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class BetResult(str, enum.Enum):
    pending = "pending"
    win = "win"
    loss = "loss"
    void = "void"
    cashout = "cashout"


class Bet(Base):
    __tablename__ = "bets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    ordem_id = Column(String(16), unique=True, index=True, nullable=False, default=lambda: uuid.uuid4().hex[:16])
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
