from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.user import User

from app.services.lesson_progress_service import complete_lesson


router = APIRouter(
    prefix="/progress",
    tags=["Progress"],
)


@router.post("/complete-lesson/{lesson_id}")
def lesson_completed(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return complete_lesson(
        db=db,
        current_user=current_user,
        lesson_id=lesson_id,
    )