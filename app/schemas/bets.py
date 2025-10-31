"""Pydantic schemas for bet resources."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator

from app.models.bets import BetResult


class BetBase(BaseModel):
    user_id: str = Field(
        ...,
        example="user-123",
        description="Identificador único do usuário proprietário da aposta.",
    )
    event: str = Field(
        ...,
        example="Flamengo vs Palmeiras",
        description="Nome do evento esportivo.",
    )
    market: str = Field(
        ...,
        example="Resultado Final",
        description="Mercado de aposta selecionado.",
    )
    odd: float = Field(
        ...,
        example=1.95,
        description="Odd (cotação) utilizada na aposta.",
    )
    stake: float = Field(
        ...,
        example=100.0,
        description="Valor apostado.",
    )
    payout_value: Optional[float] = Field(
        None,
        example=195.0,
        description="Valor retornado pela aposta (caso já conhecido).",
    )
    profit: Optional[float] = Field(
        None,
        example=95.0,
        description="Lucro obtido (calculado automaticamente quando possível).",
    )
    result: BetResult = Field(
        BetResult.pending,
        example=BetResult.pending,
        description="Resultado atual da aposta.",
    )
    is_live: bool = Field(
        False,
        example=False,
        description="Indica se a aposta foi realizada em evento ao vivo.",
    )
    source: str = Field(
        ...,
        example="mobile-app",
        description="Origem da aposta no sistema.",
    )
    image_url: Optional[str] = Field(
        None,
        example="https://cdn.calebet.app/bets/123.png",
        description="URL de uma captura de tela do comprovante da aposta.",
    )

    @root_validator
    def calculate_profit(cls, values: dict) -> dict:
        payout_value = values.get("payout_value")
        stake = values.get("stake")
        if payout_value is not None and stake is not None:
            values["profit"] = payout_value - stake
        return values


class BetCreate(BetBase):
    """Schema para criar uma aposta.

    Exemplo de corpo de requisição para ``POST /bets`` e ``POST /ingest``::

        {
            "user_id": "user-123",
            "event": "Flamengo vs Palmeiras",
            "market": "Resultado Final",
            "odd": 1.95,
            "stake": 100.0,
            "payout_value": 195.0,
            "result": "pending",
            "is_live": false,
            "source": "mobile-app",
            "image_url": "https://cdn.calebet.app/bets/123.png"
        }
    """

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user-123",
                "event": "Flamengo vs Palmeiras",
                "market": "Resultado Final",
                "odd": 1.95,
                "stake": 100.0,
                "payout_value": 195.0,
                "result": "pending",
                "is_live": False,
                "source": "mobile-app",
                "image_url": "https://cdn.calebet.app/bets/123.png",
            }
        }


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
