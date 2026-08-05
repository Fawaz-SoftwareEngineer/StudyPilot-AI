from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.course_progress import CourseProgress
from app.models.lesson import Lesson
from app.models.lesson_progress import LessonProgress


def update_course_progress(
    db: Session,
    user_id: int,
    course_id: int,
):
    """
    Recalculate and update a user's progress for a course.
    This function does NOT commit the transaction.
    """

    print("\n========== COURSE PROGRESS ==========")
    print(f"user_id = {user_id}")
    print(f"course_id = {course_id}")

    # ---------------------------------
    # Total lessons in the course
    # ---------------------------------

    total_lessons = (
        db.query(Lesson)
        .join(Lesson.module)
        .filter(
            Lesson.module.has(course_id=course_id)
        )
        .count()
    )

    print(f"total_lessons = {total_lessons}")

    # ---------------------------------
    # Completed lessons by the user
    # ---------------------------------

    completed_lessons = (
        db.query(LessonProgress)
        .join(
            Lesson,
            Lesson.id == LessonProgress.lesson_id,
        )
        .join(Lesson.module)
        .filter(
            LessonProgress.user_id == user_id,
            LessonProgress.completed == True,
            Lesson.module.has(course_id=course_id),
        )
        .count()
    )

    print(f"completed_lessons = {completed_lessons}")

    # ---------------------------------
    # Calculate completion percentage
    # ---------------------------------

    percentage = 0

    if total_lessons > 0:
        percentage = round(
            (completed_lessons / total_lessons) * 100
        )

    print(f"percentage = {percentage}")

    # ---------------------------------
    # Find existing progress
    # ---------------------------------

    progress = (
        db.query(CourseProgress)
        .filter(
            CourseProgress.user_id == user_id,
            CourseProgress.course_id == course_id,
        )
        .first()
    )

    print(f"existing progress = {progress}")

    # ---------------------------------
    # Create progress if missing
    # ---------------------------------

    if progress is None:

        print("Creating new CourseProgress row...")

        progress = CourseProgress(
            user_id=user_id,
            course_id=course_id,
        )

        db.add(progress)

    else:

        print("Updating existing CourseProgress row...")

    # ---------------------------------
    # Update progress
    # ---------------------------------

    progress.total_lessons = total_lessons
    progress.completed_lessons = completed_lessons
    progress.percentage = percentage

    if percentage == 100 and total_lessons > 0:

        progress.completed = True
        progress.completed_at = datetime.now(
            timezone.utc
        )

    else:

        progress.completed = False
        progress.completed_at = None

    print("Progress values assigned:")
    print(f"  total_lessons = {progress.total_lessons}")
    print(f"  completed_lessons = {progress.completed_lessons}")
    print(f"  percentage = {progress.percentage}")
    print(f"  completed = {progress.completed}")

    # ---------------------------------
    # Flush only (caller commits)
    # ---------------------------------

    print("Calling db.flush()...")

    db.flush()

    print("db.flush() successful!")

    print(f"CourseProgress ID = {progress.id}")

    print("========== END COURSE PROGRESS ==========\n")