from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate


def create_course(
    db: Session,
    course: CourseCreate,
):

    new_course = Course(
        title=course.title,
        description=course.description,
        subject=course.subject,
        difficulty=course.difficulty,
        thumbnail=course.thumbnail,
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


def get_all_courses(db: Session):

    return (
        db.query(Course)
        .order_by(Course.id)
        .all()
    )


def get_course(
    db: Session,
    course_id: int,
):

    return (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )