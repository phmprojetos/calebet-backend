from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Bet
from app.schemas.stats import BetStats, MarketStats
from app.utils.date_filters import resolve_date_range

router = APIRouter(prefix="/stats", tags=["Estatísticas"])


@router.get("/{user_id}", response_model=BetStats)
def get_user_stats(
    user_id: str,
    filter: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Bet).filter(Bet.user_id == user_id)

    date_range = resolve_date_range(filter, start_date, end_date)
    if date_range:
        start, end = date_range
        query = query.filter(Bet.created_at >= start, Bet.created_at <= end)

    bets = query.all()
    if not bets:
        raise HTTPException(status_code=404, detail="Nenhuma aposta encontrada")

    total_bets = len(bets)
    total_stake = sum(b.stake or 0 for b in bets)
    total_profit = sum(b.profit or 0 for b in bets)
    avg_odd = sum(b.odd or 0 for b in bets) / total_bets if total_bets else 0

    wins = [b for b in bets if b.result == "win"]
    losses = [b for b in bets if b.result == "loss"]
    cashouts = [b for b in bets if b.result == "cashout"]
    positive_cashouts = [b for b in cashouts if (b.profit or 0) > 0]

    def round_percentage(value: float) -> float:
        """Round percentage values to two decimal places."""

        return float(f"{value:.2f}")

    win_rate = (len(wins) / total_bets * 100) if total_bets else 0
    roi = ((total_profit / total_stake) * 100) if total_stake else 0

    by_result = {
        "win": len(wins),
        "loss": len(losses),
        "pending": len([b for b in bets if b.result == "pending"]),
        "void": len([b for b in bets if b.result == "void"]),
        "cashout": len(cashouts),
    }

    by_market = {}
    for b in bets:
        if not b.market:
            continue
        market = b.market
        if market not in by_market:
            by_market[market] = {
                "total_bets": 0,
                "wins": 0,
                "losses": 0,
                "cashouts": 0,
                "cashouts_positive": 0,
                "total_stake": 0.0,
                "total_profit": 0.0,
            }

        m = by_market[market]
        m["total_bets"] += 1
        m["total_stake"] += b.stake or 0
        m["total_profit"] += b.profit or 0
        if b.result == "win":
            m["wins"] += 1
        elif b.result == "loss":
            m["losses"] += 1
        elif b.result == "cashout":
            m["cashouts"] += 1
            if (b.profit or 0) > 0:
                m["cashouts_positive"] += 1

    for k, v in by_market.items():
        total_bets_m = v["total_bets"]
        total_stake_m = v["total_stake"]
        total_profit_m = v["total_profit"]
        win_rate_m = (v["wins"] / total_bets_m * 100) if total_bets_m else 0
        roi_m = ((total_profit_m / total_stake_m) * 100) if total_stake_m else 0
        by_market[k] = MarketStats(
            **v,
            win_rate=round_percentage(win_rate_m),
            roi=round_percentage(roi_m),
        )

    best_market = max(by_market.items(), key=lambda x: x[1].win_rate, default=(None, None))[0]
    worst_market = max(by_market.items(), key=lambda x: x[1].losses, default=(None, None))[0]

    return BetStats(
        total_bets=total_bets,
        total_stake=round(total_stake, 2),
        total_profit=round(total_profit, 2),
        avg_odd=round(avg_odd, 2),
        win_rate=round_percentage(win_rate),
        roi=round_percentage(roi),
        by_result=by_result,
        by_market=by_market,
        best_market=best_market,
        worst_market=worst_market,
        positive_cashouts=len(positive_cashouts),
        positive_cashouts_profit=round(sum(b.profit or 0 for b in positive_cashouts), 2),
    )
