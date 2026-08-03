from sqlalchemy.orm import Session

from app.models.user import User


XP_PER_LEVEL = 100


def calculate_level(xp: int) -> int:
    return (xp // XP_PER_LEVEL) + 1


def award_xp(
    db: Session,
    user: User,
    amount: int,
) -> User:

    user.xp += amount
    user.level = calculate_level(user.xp)

    db.commit()
    db.refresh(user)

    return user


def award_coins(
    db: Session,
    user: User,
    amount: int,
) -> User:

    user.coins += amount

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

    db.commit()
    db.refresh(user)

    return user