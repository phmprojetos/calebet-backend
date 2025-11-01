"""Populate missing ordem_id values for existing bets."""

import uuid

from app.db import SessionLocal
from app.models import Bet


def main() -> None:
    db = SessionLocal()
    try:
        bets = db.query(Bet).filter(Bet.ordem_id.is_(None)).all()
        for bet in bets:
            bet.ordem_id = uuid.uuid4().hex[:16]
        if bets:
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
