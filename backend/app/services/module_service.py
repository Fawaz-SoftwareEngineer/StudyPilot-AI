from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.module import Module
from app.schemas.module import ModuleCreate


def create_module(
    db: Session,
    module: ModuleCreate,
):
    course = (
        db.query(Course)
        .filter(Course.id == module.course_id)
        .first()
    )

    if course is None:
        raise ValueError("Course not found")

    new_module = Module(
        course_id=module.course_id,
        title=module.title,
        description=module.description,
        module_order=module.module_order,
    )

    db.add(new_module)
    db.commit()
    db.refresh(new_module)

    return new_module


def get_module(
    db: Session,
    module_id: int,
):
    return (
        db.query(Module)
        .filter(Module.id == module_id)
        .first()
    )


def get_course_modules(
    db: Session,
    course_id: int,
):
    return (
        db.query(Module)
        .filter(Module.course_id == course_id)
        .order_by(Module.module_order)
        .all()
    )