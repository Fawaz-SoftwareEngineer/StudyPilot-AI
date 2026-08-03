from app.models.user import User


def get_dashboard(user: User):
    return {
        "full_name": user.full_name,
        "level": user.level,
        "xp": user.xp,
        "coins": user.coins,
        "streak": user.streak,
        "completed_lessons": user.completed_lessons,
    }