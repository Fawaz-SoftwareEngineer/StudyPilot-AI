from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_admin_or_teacher
from app.models.user import User

from app.schemas.question_option import (
    QuestionOptionCreate,
    QuestionOptionResponse,
)

from app.services.question_option_service import (
    create_option,
    get_question_options,
)

router = APIRouter(
    prefix="/question-options",
    tags=["Question Options"],
)


@router.post(
    "/",
    response_model=QuestionOptionResponse,
)
def add_option(
    option: QuestionOptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_teacher),
):
    try:
        return create_option(db, option)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/question/{question_id}",
    response_model=list[QuestionOptionResponse],
)
def list_options(
    question_id: int,
    db: Session = Depends(get_db),
):
    return get_question_options(
        db,
        question_id,
    )