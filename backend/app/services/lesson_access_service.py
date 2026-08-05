from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.lesson_progress import LessonProgress


def can_access_lesson(
    db: Session,
    user_id: int,
    lesson: Lesson,
) -> bool:
    """
    Returns True if the lesson is unlocked.

    Rules:
    - First lesson of the first module is always unlocked.
    - Other lessons require the previous lesson in the same module.
    - First lesson of a later module requires the final lesson
      of the previous module.
    """

    course = lesson.module.course

    modules = sorted(
        course.modules,
        key=lambda m: m.module_order,
    )

    current_module_index = next(
        (
            i
            for i, m in enumerate(modules)
            if m.id == lesson.module.id
        ),
        None,
    )

    if current_module_index is None:
        return False

    current_module = modules[current_module_index]

    lessons = sorted(
        current_module.lessons,
        key=lambda l: l.lesson_order,
    )

    lesson_index = next(
        (
            i
            for i, l in enumerate(lessons)
            if l.id == lesson.id
        ),
        None,
    )

    if lesson_index is None:
        return False

    # ------------------------------------------------
    # First lesson of first module
    # ------------------------------------------------

    if current_module_index == 0 and lesson_index == 0:
        return True

    # ------------------------------------------------
    # First lesson of any later module
    # ------------------------------------------------

    if lesson_index == 0:

        previous_module = modules[current_module_index - 1]

        previous_lessons = sorted(
            previous_module.lessons,
            key=lambda l: l.lesson_order,
        )

        if not previous_lessons:
            return False

        previous_last_lesson = previous_lessons[-1]

        progress = (
            db.query(LessonProgress)
            .filter(
                LessonProgress.user_id == user_id,
                LessonProgress.lesson_id == previous_last_lesson.id,
                LessonProgress.completed == True,
            )
            .first()
        )

        return progress is not None

    # ------------------------------------------------
    # Other lessons
    # ------------------------------------------------

    previous_lesson = lessons[lesson_index - 1]

    progress = (
        db.query(LessonProgress)
        .filter(
            LessonProgress.user_id == user_id,
            LessonProgress.lesson_id == previous_lesson.id,
            LessonProgress.completed == True,
        )
        .first()
    )

    return progress is not None