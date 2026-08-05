from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.lesson_progress import LessonProgress
from app.models.user import User

from app.services.achievement_service import unlock_achievement
from app.services.course_progress_service import update_course_progress


def complete_lesson(
    db: Session,
    current_user: User,
    lesson_id: int,
):
    """
    Marks a lesson as completed, rewards the user,
    updates course progress, and unlocks achievements.
    """

    # -------------------------
    # Find lesson
    # -------------------------

    lesson = (
        db.query(Lesson)
        .filter(Lesson.id == lesson_id)
        .first()
    )

    if lesson is None:
        raise ValueError("Lesson not found")

    # -------------------------
    # Prevent duplicate completion
    # -------------------------

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

    # -------------------------
    # Create lesson progress
    # -------------------------

    progress = LessonProgress(
        user_id=current_user.id,
        lesson_id=lesson.id,
        completed=True,
        completed_at=datetime.now(timezone.utc),
    )

    db.add(progress)

    # -------------------------
    # Rewards
    # -------------------------

    current_user.xp += lesson.xp_reward
    current_user.coins += 10
    current_user.completed_lessons += 1

    # Update level
    current_user.level = (current_user.xp // 100) + 1

    # -------------------------
    # Unlock achievements
    # -------------------------

    if current_user.completed_lessons == 1:
        unlock_achievement(
            db=db,
            user=current_user,
            achievement_name="First Lesson",
        )

    # -------------------------
    # Update course progress
    # -------------------------

    update_course_progress(
        db=db,
        user_id=current_user.id,
        course_id=lesson.module.course_id,
    )

    # -------------------------
    # Save everything
    # -------------------------

    try:
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