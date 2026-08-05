from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate

from sqlalchemy.orm import joinedload

from app.models.module import Module

from app.models.lesson_progress import LessonProgress
from app.models.lesson import Lesson

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

def get_course_details(
    db: Session,
    course_id: int,
    user_id: int,
):
    course = (
        db.query(Course)
        .options(
            joinedload(Course.modules)
            .joinedload(Module.lessons)
            .joinedload(Lesson.quiz)
        )
        .filter(Course.id == course_id)
        .first()
    )

    if course is None:
        return None

    completed_lessons = {
        progress.lesson_id
        for progress in db.query(LessonProgress)
        .filter(
            LessonProgress.user_id == user_id,
            LessonProgress.completed == True,
        )
        .all()
    }

    modules_data = []

    for module in sorted(
        course.modules,
        key=lambda m: m.module_order,
    ):

        lessons = sorted(
            module.lessons,
            key=lambda l: l.lesson_order,
        )

        lessons_data = []

        for index, lesson in enumerate(lessons):

            completed = lesson.id in completed_lessons

            if index == 0:
                locked = False
            else:
                previous_lesson = lessons[index - 1]
                locked = previous_lesson.id not in completed_lessons

            lessons_data.append(
                {
                    "id": lesson.id,
                    "title": lesson.title,
                    "lesson_order": lesson.lesson_order,
                    "completed": completed,
                    "locked": locked,
                    "has_quiz": lesson.quiz is not None,
                }
            )

        modules_data.append(
            {
                "id": module.id,
                "title": module.title,
                "description": module.description,
                "module_order": module.module_order,
                "lessons": lessons_data,
            }
        )

    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "subject": course.subject,
        "difficulty": course.difficulty,
        "modules": modules_data,
    }