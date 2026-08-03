from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_admin_or_teacher
from app.models.user import User
from app.schemas.question import (
    QuestionCreate,
    QuestionResponse,
)
from app.services.question_service import (
    create_question,
    get_questions_by_quiz,
)

router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.post("/", response_model=QuestionResponse)
def add_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_teacher),
):
    try:
        return create_question(db, question)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/quiz/{quiz_id}",
            response_model=list[QuestionResponse])
def list_questions(
    quiz_id: int,
    db: Session = Depends(get_db),
):
    return get_questions_by_quiz(
        db,
        quiz_id,
    )