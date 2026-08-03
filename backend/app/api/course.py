from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.permissions import require_admin_or_teacher
from app.models.user import User

from app.schemas.course import (
    CourseCreate,
    CourseResponse,
)

from app.services.course_service import (
    create_course,
    get_all_courses,
    get_course,
)

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.post(
    "/",
    response_model=CourseResponse,
)
def create_new_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_teacher),
):
    return create_course(db, course)


@router.get(
    "/",
    response_model=list[CourseResponse],
)
def list_courses(
    db: Session = Depends(get_db),
):
    return get_all_courses(db)


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
)
def get_single_course(
    course_id: int,
    db: Session = Depends(get_db),
):

    course = get_course(
        db,
        course_id,
    )

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return course