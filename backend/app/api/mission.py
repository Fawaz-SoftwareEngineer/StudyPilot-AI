from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi import Depends

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.user import User

from app.schemas.mission import (
    MissionCreate,
    MissionResponse,
    UserMissionResponse,
)

from app.services.mission_service import (
    create_mission,
    list_missions,
    assign_daily_missions,
    get_user_missions,
    claim_mission_reward,
)

router = APIRouter(
    prefix="/missions",
    tags=["Missions"],
)

@router.post(
    "/",
    response_model=MissionResponse,
)
def add_mission(
    mission: MissionCreate,
    db: Session = Depends(get_db),
):
    return create_mission(
        db=db,
        mission=mission,
    )

@router.get(
    "/",
    response_model=list[MissionResponse],
)
def all_missions(
    db: Session = Depends(get_db),
):
    return list_missions(db)

@router.post(
    "/assign-daily",
)
def assign_my_daily_missions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    assign_daily_missions(
        db=db,
        user=current_user,
    )

    return {
        "message": "Daily missions assigned."
    }

@router.get(
    "/me",
    response_model=list[UserMissionResponse],
)
def my_missions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return get_user_missions(
        db=db,
        user=current_user,
    )

@router.post(
    "/claim/{user_mission_id}",
    response_model=UserMissionResponse,
)
def claim_reward(
    user_mission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return claim_mission_reward(
        db=db,
        user=current_user,
        user_mission_id=user_mission_id,
    )