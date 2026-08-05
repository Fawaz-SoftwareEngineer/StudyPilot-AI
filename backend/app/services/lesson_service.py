from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.module import Module
from app.schemas.lesson import LessonCreate


def create_lesson(
    db: Session,
    lesson: LessonCreate,
):
    module = (
        db.query(Module)
        .filter(Module.id == lesson.module_id)
        .first()
    )

    if module is None:
        raise ValueError("Module not found")

    new_lesson = Lesson(
        module_id=lesson.module_id,
        title=lesson.title,
        content=lesson.content,
        lesson_order=lesson.lesson_order,
        xp_reward=lesson.xp_reward,
    )

    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)

    return new_lesson


def get_lesson(
    db: Session,
    lesson_id: int,
):
    return (
        db.query(Lesson)
        .filter(Lesson.id == lesson_id)
        .first()
    )


def get_module_lessons(
    db: Session,
    module_id: int,
):
    return (
        db.query(Lesson)
        .filter(Lesson.module_id == module_id)
        .order_by(Lesson.lesson_order)
        .all()
    )