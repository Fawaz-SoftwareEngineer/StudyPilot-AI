from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.user import User

from app.schemas.quiz_analytics import QuizAnalyticsResponse

from app.services.quiz_analytics_service import (
    get_quiz_analytics,
)


router = APIRouter(
    prefix="/quiz-analytics",
    tags=["Quiz Analytics"],
)


@router.get(
    "/",
    response_model=QuizAnalyticsResponse,
)
def quiz_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_quiz_analytics(
        db=db,
        current_user=current_user,
    )