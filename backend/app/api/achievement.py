from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_admin_or_teacher
from app.core.security import get_current_user

from app.models.user import User

from app.schemas.achievement import (
    AchievementCreate,
    AchievementResponse,
    UserAchievementResponse,
)

from app.services.achievement_service import (
    create_achievement,
    get_all_achievements,
    get_user_achievements,
)

router = APIRouter(
    prefix="/achievements",
    tags=["Achievements"],
)


@router.post(
    "/",
    response_model=AchievementResponse,
)
def add_achievement(
    achievement: AchievementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_teacher),
):
    return create_achievement(
        db,
        achievement,
    )


@router.get(
    "/",
    response_model=list[AchievementResponse],
)
def list_achievements(
    db: Session = Depends(get_db),
):
    return get_all_achievements(db)


@router.get(
    "/me",
    response_model=list[UserAchievementResponse],
)
def my_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_achievements(
        db,
        current_user,
    )