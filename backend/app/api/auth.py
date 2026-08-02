from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserLogin
from app.services.auth_service import login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        user = UserLogin(
            email=form_data.username,
            password=form_data.password,
        )

        return login_user(db, user)

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )