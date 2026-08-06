from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserMission(Base):
    __tablename__ = "user_missions"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )

    mission_id: Mapped[int] = mapped_column(
        ForeignKey(
            "missions.id",
            ondelete="CASCADE",
        )
    )

    current_progress: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    claimed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime
    )

    user = relationship(
        "User",
        back_populates="missions",
    )

    mission = relationship(
        "Mission",
        back_populates="user_missions",
    )