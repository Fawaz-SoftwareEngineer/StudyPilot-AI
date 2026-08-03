from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.xp_service import complete_lesson

router = APIRouter(
    prefix="/progress",
    tags=["Progress"],
)


@router.post("/complete-lesson")
def lesson_completed(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    updated_user = complete_lesson(
        db,
        current_user,
    )

    return {
        "message": "Lesson completed!",
        "xp": updated_user.xp,
        "level": updated_user.level,
        "coins": updated_user.coins,
        "completed_lessons": updated_user.completed_lessons,
    }