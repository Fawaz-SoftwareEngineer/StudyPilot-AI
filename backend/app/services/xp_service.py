from sqlalchemy.orm import Session

from app.models.user import User

from app.services.mission_service import update_mission_progress

from app.models.xp_history import XPHistory
from app.models.coin_history import CoinHistory

XP_PER_LEVEL = 100


def calculate_level(xp: int) -> int:
    return (xp // XP_PER_LEVEL) + 1


def award_xp(
    db: Session,
    user: User,
    amount: int,
    source: str,
) -> User:

    user.xp += amount
    user.level = calculate_level(user.xp)

    db.add(
        XPHistory(
            user_id=user.id,
            amount=amount,
            source=source,
        )
    )

    update_mission_progress(
        db=db,
        user=user,
        mission_type="earn_xp",
        amount=amount,
    )

    db.commit()
    db.refresh(user)

    return user

def award_coins(
    db: Session,
    user: User,
    amount: int,
    source: str,
) -> User:

    user.coins += amount

    db.add(
        CoinHistory(
            user_id=user.id,
            amount=amount,
            source=source,
        )
    )

    db.commit()
    db.refresh(user)

    return user


def increase_streak(
    db: Session,
    user: User,
) -> User:

    user.streak += 1

    db.commit()
    db.refresh(user)

    return user


def complete_lesson(
    db: Session,
    user: User,
) -> User:

    user.completed_lessons += 1
    user.xp += 25
    user.coins += 10
    user.level = calculate_level(user.xp)

    update_mission_progress(
        db=db,
        user=user,
        mission_type="lesson_completed",
    )

    db.commit()
    db.refresh(user)

    return user