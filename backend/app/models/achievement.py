from sqlalchemy import Integer, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
    )

    description: Mapped[str] = mapped_column(
        String(500),
    )

    icon: Mapped[str] = mapped_column(
        String(100),
        default="🏆",
    )

    xp_reward: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    coins_reward: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    users = relationship(
        "UserAchievement",
        back_populates="achievement",
        cascade="all, delete-orphan",
    )