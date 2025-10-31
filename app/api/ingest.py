"""API endpoints for ingesting bet data."""

from __future__ import annotations

import io
from typing import Any, Dict

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.bets import Bet
from app.schemas.bets import BetCreate, BetRead


router = APIRouter(tags=["Ingest"])


@router.post("/ingest", response_model=BetRead)
def ingest_bet(payload: BetCreate, db: Session = Depends(get_db)) -> Bet:
    """Insert a single bet record provided as JSON."""

    bet_data = payload.dict()
    if payload.payout_value is not None:
        bet_data["profit"] = payload.payout_value - payload.stake

    bet = Bet(**bet_data)
    db.add(bet)
    db.commit()
    db.refresh(bet)
    return bet


def _sanitize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Convert NaN values to ``None`` so they are acceptable for the ORM."""

    sanitized: Dict[str, Any] = {}
    for key, value in record.items():
        if pd.isna(value):  # type: ignore[arg-type]
            sanitized[key] = None
        else:
            sanitized[key] = value
    return sanitized


@router.post("/import/csv")
async def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict[str, int]:
    """Import bet data from a CSV file."""

    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    try:
        contents = await file.read()
        dataframe = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=400, detail="Unable to read CSV file.") from exc

    required_columns = {"user_id", "source", "event", "market", "odd", "stake"}
    missing_columns = required_columns - set(dataframe.columns)
    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {', '.join(sorted(missing_columns))}",
        )

    inserted = 0
    bet_models: list[Bet] = []
    for record in dataframe.to_dict(orient="records"):
        sanitized = _sanitize_record(record)
        bet_schema = BetCreate(**{k: v for k, v in sanitized.items() if v is not None})
        bet_data = bet_schema.dict()
        if bet_schema.payout_value is not None:
            bet_data["profit"] = bet_schema.payout_value - bet_schema.stake
        bet_models.append(Bet(**bet_data))
        inserted += 1

    if bet_models:
        db.add_all(bet_models)
        db.commit()

    return {"inserted": inserted}

