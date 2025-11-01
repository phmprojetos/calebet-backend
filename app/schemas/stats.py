from pydantic import BaseModel
from typing import Dict, Optional


class MarketStats(BaseModel):
    total_bets: int
    wins: int
    losses: int
    cashouts: int
    cashouts_positive: int
    total_stake: float
    total_profit: float
    win_rate: float
    roi: float


class BetStats(BaseModel):
    total_bets: int
    total_stake: float
    total_profit: float
    avg_odd: float
    win_rate: float
    roi: float
    by_result: dict
    by_market: Dict[str, MarketStats]
    best_market: Optional[str]
    worst_market: Optional[str]
    positive_cashouts: int
    positive_cashouts_profit: float
