from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_admin_or_teacher
from app.core.security import get_current_user

from app.models.user import User

from app.schemas.lesson import (
    LessonCreate,
    LessonResponse,
)

from app.services.lesson_service import (
    create_lesson,
    get_lesson,
    get_module_lessons,
)

from app.services.lesson_access_service import (
    can_access_lesson,
)

router = APIRouter(
    prefix="/lessons",
    tags=["Lessons"],
)


@router.post(
    "/",
    response_model=LessonResponse,
)
def add_lesson(
    lesson: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_teacher),
):
    try:
        return create_lesson(
            db,
            lesson,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/{lesson_id}",
    response_model=LessonResponse,
)
def read_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lesson = get_lesson(
        db,
        lesson_id,
    )

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found",
        )

    if not can_access_lesson(
        db=db,
        user_id=current_user.id,
        lesson=lesson,
    ):
        raise HTTPException(
            status_code=403,
            detail="Complete previous lessons first.",
        )

    return lesson


@router.get(
    "/module/{module_id}",
    response_model=list[LessonResponse],
)
def list_module_lessons(
    module_id: int,
    db: Session = Depends(get_db),
):
    return get_module_lessons(
        db,
        module_id,
    )