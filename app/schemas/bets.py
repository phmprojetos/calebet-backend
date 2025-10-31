"""Pydantic schemas for bet resources."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, root_validator

from app.models.bets import BetResult


class BetBase(BaseModel):
    user_id: str
    event: str
    market: str
    odd: float
    stake: float
    payout_value: Optional[float] = None
    profit: Optional[float] = None
    result: BetResult = BetResult.pending
    is_live: bool = False
    source: str
    image_url: Optional[str] = None

    @root_validator
    def calculate_profit(cls, values: dict) -> dict:
        payout_value = values.get("payout_value")
        stake = values.get("stake")
        if payout_value is not None and stake is not None:
            values["profit"] = payout_value - stake
        return values


class BetCreate(BetBase):
    """Schema for creating a bet."""


class BetUpdate(BaseModel):
    """Schema for updating an existing bet."""

    user_id: Optional[str] = None
    event: Optional[str] = None
    market: Optional[str] = None
    odd: Optional[float] = None
    stake: Optional[float] = None
    payout_value: Optional[float] = None
    profit: Optional[float] = None
    result: Optional[BetResult] = None
    is_live: Optional[bool] = None
    source: Optional[str] = None
    image_url: Optional[str] = None

    @root_validator
    def calculate_profit(cls, values: dict) -> dict:
        payout_value = values.get("payout_value")
        stake = values.get("stake")
        if payout_value is not None and stake is not None:
            values["profit"] = payout_value - stake
        return values


class BetRead(BetBase):
    """Schema returned when reading bet information."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
