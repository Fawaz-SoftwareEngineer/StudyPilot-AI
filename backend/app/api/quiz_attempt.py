from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.user import User

from app.schemas.quiz_attempt import (
    QuizSubmission,
    QuizResult,
)

from app.services.quiz_attempt_service import submit_quiz

router = APIRouter(
    prefix="/quiz-attempts",
    tags=["Quiz Attempts"],
)


@router.post(
    "/submit",
    response_model=QuizResult,
)
def submit(
    submission: QuizSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:
        return submit_quiz(
            db,
            current_user,
            submission,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )