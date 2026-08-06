from sqlalchemy.orm import Session

from app.models.coin_history import CoinHistory
from app.models.user import User


def add_coin_history(
    db: Session,
    user: User,
    amount: int,
    reason: str,
) -> CoinHistory:

    history = CoinHistory(
        user_id=user.id,
        amount=amount,
        reason=reason,
    )

    db.add(history)

    return history


def get_coin_history(
    db: Session,
    user: User,
) -> list[CoinHistory]:

    return (
        db.query(CoinHistory)
        .filter(
            CoinHistory.user_id == user.id
        )
        .order_by(
            CoinHistory.created_at.desc()
        )
        .all()
    )