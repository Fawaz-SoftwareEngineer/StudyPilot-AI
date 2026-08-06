from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.user import User

from app.schemas.quiz_review import QuizReview

from app.services.quiz_review_service import get_quiz_review

router = APIRouter(
    prefix="/quiz-review",
    tags=["Quiz Review"],
)


@router.get(
    "/{attempt_id}",
    response_model=QuizReview,
)
def review_quiz(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_quiz_review(
        db=db,
        current_user=current_user,
        attempt_id=attempt_id,
    )