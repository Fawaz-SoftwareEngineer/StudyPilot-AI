from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.course_progress import CourseProgress
from app.models.lesson import Lesson
from app.models.lesson_progress import LessonProgress


def update_course_progress(
    db: Session,
    user_id: int,
    course_id: int,
):
    """
    Recalculate a user's progress for a course.
    """

    total_lessons = (
        db.query(Lesson)
        .join(
            Lesson.module
        )
        .filter(
            Lesson.module.has(course_id=course_id)
        )
        .count()
    )

    completed_lessons = (
        db.query(LessonProgress)
        .join(
            Lesson,
            Lesson.id == LessonProgress.lesson_id,
        )
        .join(
            Lesson.module
        )
        .filter(
            LessonProgress.user_id == user_id,
            LessonProgress.completed == True,
            Lesson.module.has(course_id=course_id),
        )
        .count()
    )

    percentage = 0

    if total_lessons > 0:
        percentage = round(
            (completed_lessons / total_lessons) * 100
        )

    progress = (
        db.query(CourseProgress)
        .filter(
            CourseProgress.user_id == user_id,
            CourseProgress.course_id == course_id,
        )
        .first()
    )

    if progress is None:

        progress = CourseProgress(
            user_id=user_id,
            course_id=course_id,
        )

        db.add(progress)

    progress.total_lessons = total_lessons
    progress.completed_lessons = completed_lessons
    progress.percentage = percentage

    if percentage == 100:
        progress.completed = True
        progress.completed_at = datetime.utcnow()
    else:
        progress.completed = False
        progress.completed_at = None