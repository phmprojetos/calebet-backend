from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.bets import Bet
from app.schemas.bets import BetCreate, BetRead, BetUpdate

router = APIRouter(prefix="/bets", tags=["Bets"])

@router.post("/", response_model=BetRead)
def create_bet(bet: BetCreate, db: Session = Depends(get_db)):
    """Criar uma nova aposta.

    Exemplo de requisição::

        POST /bets
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

    db_bet = Bet(**bet.model_dump())
    if bet.payout_value:
        db_bet.profit = bet.payout_value - bet.stake
    db.add(db_bet)
    db.commit()
    db.refresh(db_bet)
    return db_bet

@router.get("/", response_model=list[BetRead])
def list_bets(user_id: str = None, db: Session = Depends(get_db)):
    q = db.query(Bet)
    if user_id:
        q = q.filter(Bet.user_id == user_id)
    return q.order_by(Bet.created_at.desc()).all()

@router.get("/{ordem_id}", response_model=BetRead)
def get_bet(ordem_id: str, db: Session = Depends(get_db)):
    bet = db.query(Bet).filter(Bet.ordem_id == ordem_id).first()
    if not bet:
        raise HTTPException(status_code=404, detail="Bet not found")
    return bet

@router.patch("/{ordem_id}", response_model=BetRead)
def update_bet(ordem_id: str, update: BetUpdate, db: Session = Depends(get_db)):
    bet = db.query(Bet).filter(Bet.ordem_id == ordem_id).first()
    if not bet:
        raise HTTPException(status_code=404, detail="Bet not found")
    for k, v in update.model_dump(exclude_unset=True).items():
        setattr(bet, k, v)
    if update.payout_value is not None:
        bet.profit = update.payout_value - bet.stake
    db.commit()
    db.refresh(bet)
    return bet

@router.delete("/{ordem_id}")
def delete_bet(ordem_id: str, db: Session = Depends(get_db)):
    bet = db.query(Bet).filter(Bet.ordem_id == ordem_id).first()
    if not bet:
        raise HTTPException(status_code=404, detail="Bet not found")
    db.delete(bet)
    db.commit()
    return {"deleted": True}
