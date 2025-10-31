"""Pydantic models for bet resources."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class BetBase(BaseModel):
    event: str = Field(..., description="Event name for the bet")
    market: str = Field(..., description="Market of the bet")
    selection: str = Field(..., description="Selection taken in the bet")
    odds: Decimal = Field(..., description="Odds offered for the selection")
    stake: Decimal = Field(..., description="Stake placed on the bet")


class BetCreate(BetBase):
    """Schema for creating a bet."""


class BetRead(BetBase):
    """Schema returned when reading bet information."""

    id: int
    created_at: datetime

    class Config:
        orm_mode = True
