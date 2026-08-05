from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_admin_or_teacher

from app.models.user import User

from app.schemas.module import (
    ModuleCreate,
    ModuleResponse,
)

from app.services.module_service import (
    create_module,
    get_module,
    get_course_modules,
)

router = APIRouter(
    prefix="/modules",
    tags=["Modules"],
)


@router.post("/", response_model=ModuleResponse)
def add_module(
    module: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_teacher),
):
    try:
        return create_module(db, module)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/{module_id}", response_model=ModuleResponse)
def read_module(
    module_id: int,
    db: Session = Depends(get_db),
):
    module = get_module(db, module_id)

    if module is None:
        raise HTTPException(
            status_code=404,
            detail="Module not found",
        )

    return module


@router.get(
    "/course/{course_id}",
    response_model=list[ModuleResponse],
)
def list_course_modules(
    course_id: int,
    db: Session = Depends(get_db),
):
    return get_course_modules(db, course_id)