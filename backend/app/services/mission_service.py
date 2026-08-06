from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.mission import Mission
from app.models.user import User
from app.models.user_mission import UserMission

from app.services.xp_service import (
    award_xp,
    award_coins,
)

from app.schemas.mission import MissionCreate

from app.services.xp_service import calculate_level


def create_mission(
    db: Session,
    mission: MissionCreate,
) -> Mission:

    new_mission = Mission(
        title=mission.title,
        description=mission.description,
        mission_type=mission.mission_type,
        target_value=mission.target_value,
        xp_reward=mission.xp_reward,
        coin_reward=mission.coin_reward,
        is_daily=mission.is_daily,
        is_weekly=mission.is_weekly,
    )

    db.add(new_mission)
    db.commit()
    db.refresh(new_mission)

    return new_mission


def list_missions(
    db: Session,
) -> list[Mission]:

    return (
        db.query(Mission)
        .filter(
            Mission.is_active == True
        )
        .all()
    )


def assign_daily_missions(
    db: Session,
    user: User,
) -> None:

    daily_missions = (
        db.query(Mission)
        .filter(
            Mission.is_daily == True,
            Mission.is_active == True,
        )
        .all()
    )

    tomorrow = (
        datetime.now(timezone.utc)
        + timedelta(days=1)
    )

    for mission in daily_missions:

        existing = (
            db.query(UserMission)
            .filter(
                UserMission.user_id == user.id,
                UserMission.mission_id == mission.id,
                UserMission.expires_at > datetime.now(timezone.utc),
            )
            .first()
        )

        if existing:
            continue

        db.add(
            UserMission(
                user_id=user.id,
                mission_id=mission.id,
                expires_at=tomorrow,
            )
        )

    db.commit()


def get_user_missions(
    db: Session,
    user: User,
) -> list[UserMission]:

    return (
        db.query(UserMission)
        .filter(
            UserMission.user_id == user.id
        )
        .all()
    )


def update_mission_progress(
    db: Session,
    user: User,
    mission_type: str,
    amount: int = 1,
) -> None:

    missions = (
        db.query(UserMission)
        .join(Mission)
        .filter(
            UserMission.user_id == user.id,
            UserMission.completed == False,
            UserMission.claimed == False,
            Mission.mission_type == mission_type,
        )
        .all()
    )

    for user_mission in missions:

        user_mission.current_progress += amount

        if (
            user_mission.current_progress
            >= user_mission.mission.target_value
        ):
            user_mission.current_progress = (
                user_mission.mission.target_value
            )
            user_mission.completed = True

    db.commit()


def claim_mission_reward(
    db: Session,
    user: User,
    user_mission_id: int,
) -> UserMission:

    user_mission = (
        db.query(UserMission)
        .filter(
            UserMission.id == user_mission_id,
            UserMission.user_id == user.id,
        )
        .first()
    )

    if user_mission is None:
        raise ValueError("Mission not found")

    if (
        user_mission.expires_at
        and user_mission.expires_at < datetime.now(timezone.utc)
    ):
        raise ValueError("Mission expired")

    if not user_mission.completed:
        raise ValueError("Mission not completed")

    if user_mission.claimed:
        raise ValueError("Reward already claimed")

    mission = user_mission.mission

    user_mission.claimed = True

    award_xp(
        db=db,
        user=user,
        amount=mission.xp_reward,
        source=f"Mission: {mission.title}",
    )

    award_coins(
        db=db,
        user=user,
        amount=mission.coin_reward,
        source=f"Mission: {mission.title}",
    )

    db.commit()

    db.refresh(user)
    db.refresh(user_mission)

    return user_mission