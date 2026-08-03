from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_admin_or_teacher
from app.models.user import User
from app.schemas.quiz import QuizCreate, QuizResponse
from app.services.quiz_service import (
    create_quiz,
    get_all_quizzes,
    get_quiz,
)

router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"],
)


@router.post("/", response_model=QuizResponse)
def add_quiz(
    quiz: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_teacher),
):
    try:
        return create_quiz(db, quiz)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[QuizResponse])
def list_quizzes(
    db: Session = Depends(get_db),
):
    return get_all_quizzes(db)


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_single_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
):
    quiz = get_quiz(db, quiz_id)

    if quiz is None:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )

    return quiz