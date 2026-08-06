from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.user import User

from app.services.coin_history_service import (
    get_coin_history,
)

router = APIRouter(
    prefix="/coins",
    tags=["Coin History"],
)


@router.get("/history")
def coin_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return get_coin_history(
        db=db,
        user=current_user,
    )