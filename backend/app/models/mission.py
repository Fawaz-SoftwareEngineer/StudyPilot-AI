from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(150)
    )

    description: Mapped[str] = mapped_column(
        String(500)
    )

    mission_type: Mapped[str] = mapped_column(
        String(50)
    )

    target_value: Mapped[int] = mapped_column(
        Integer
    )

    xp_reward: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    coin_reward: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    is_daily: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_weekly: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    user_missions = relationship(
        "UserMission",
        back_populates="mission",
        cascade="all, delete-orphan",
    )