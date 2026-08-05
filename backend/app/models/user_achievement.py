from datetime import datetime

from sqlalchemy import DateTime, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    achievement_id: Mapped[int] = mapped_column(
        ForeignKey("achievements.id", ondelete="CASCADE")
    )

    unlocked_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    user = relationship(
        "User",
        back_populates="achievements",
    )

    achievement = relationship(
        "Achievement",
        back_populates="users",
    )