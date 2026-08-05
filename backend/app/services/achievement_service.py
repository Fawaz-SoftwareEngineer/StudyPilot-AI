from sqlalchemy.orm import Session

from app.models.achievement import Achievement
from app.models.user import User
from app.models.user_achievement import UserAchievement

from app.schemas.achievement import AchievementCreate


def create_achievement(
    db: Session,
    achievement: AchievementCreate,
):
    new_achievement = Achievement(
        name=achievement.name,
        description=achievement.description,
        icon=achievement.icon,
        xp_reward=achievement.xp_reward,
        coins_reward=achievement.coins_reward,
    )

    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)

    return new_achievement


def get_all_achievements(
    db: Session,
):
    return (
        db.query(Achievement)
        .order_by(Achievement.id)
        .all()
    )


def get_user_achievements(
    db: Session,
    user: User,
):
    return (
        db.query(UserAchievement)
        .filter(
            UserAchievement.user_id == user.id
        )
        .all()
    )


def has_achievement(
    db: Session,
    user_id: int,
    achievement_name: str,
) -> bool:

    achievement = (
        db.query(Achievement)
        .filter(
            Achievement.name == achievement_name
        )
        .first()
    )

    if achievement is None:
        return False

    existing = (
        db.query(UserAchievement)
        .filter(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == achievement.id,
        )
        .first()
    )

    return existing is not None


def unlock_achievement(
    db: Session,
    user: User,
    achievement_name: str,
):

    achievement = (
        db.query(Achievement)
        .filter(
            Achievement.name == achievement_name
        )
        .first()
    )

    if achievement is None:
        return

    if has_achievement(
        db,
        user.id,
        achievement_name,
    ):
        return

    unlocked = UserAchievement(
        user_id=user.id,
        achievement_id=achievement.id,
    )

    db.add(unlocked)

    # Reward the user
    user.xp += achievement.xp_reward
    user.coins += achievement.coins_reward

    # Recalculate level
    user.level = (user.xp // 100) + 1