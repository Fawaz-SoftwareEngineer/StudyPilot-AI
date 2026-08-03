from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.lesson_progress import LessonProgress
from app.models.user import User


def complete_lesson(
    db: Session,
    current_user: User,
    lesson_id: int,
):
    """
    Marks a lesson as completed and rewards the user.
    """

    # Find the lesson
    lesson = (
        db.query(Lesson)
        .filter(Lesson.id == lesson_id)
        .first()
    )

    if lesson is None:
        raise ValueError("Lesson not found")

    # Check if lesson has already been completed
    existing_progress = (
        db.query(LessonProgress)
        .filter(
            LessonProgress.user_id == current_user.id,
            LessonProgress.lesson_id == lesson_id,
        )
        .first()
    )

    if existing_progress:
        raise ValueError("Lesson already completed")

    # Create lesson progress
    progress = LessonProgress(
        user_id=current_user.id,
        lesson_id=lesson.id,
        completed=True,
        completed_at=datetime.now(timezone.utc),
    )

    # Award XP
    current_user.xp += lesson.xp_reward

    # Update level
    current_user.level = (current_user.xp // 100) + 1

    # Award coins
    current_user.coins += 10

    # Increment completed lessons
    current_user.completed_lessons += 1

    try:
        db.add(progress)

        db.commit()

        db.refresh(progress)
        db.refresh(current_user)

    except Exception:
        db.rollback()
        raise

    return {
        "message": "Lesson completed successfully!",
        "lesson_id": lesson.id,
        "xp_gained": lesson.xp_reward,
        "coins_gained": 10,
        "total_xp": current_user.xp,
        "current_level": current_user.level,
        "total_coins": current_user.coins,
        "completed_lessons": current_user.completed_lessons,
    }