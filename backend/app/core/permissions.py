from fastapi import Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.user import User


def require_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user


def require_teacher(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher access required",
        )

    return current_user


def require_admin_or_teacher(
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or Teacher access required",
        )

    return current_user