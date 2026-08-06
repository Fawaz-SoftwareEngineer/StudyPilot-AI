from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    full_name: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(String(255))

    country: Mapped[str] = mapped_column(String(100))

    education_level: Mapped[str] = mapped_column(String(50))

    role: Mapped[str] = mapped_column(
        String(20),
        default="student",
    )

    xp: Mapped[int] = mapped_column(Integer, default=0)

    level: Mapped[int] = mapped_column(Integer, default=1)

    coins: Mapped[int] = mapped_column(Integer, default=100)

    streak: Mapped[int] = mapped_column(Integer, default=0)

    completed_lessons: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    lesson_progress = relationship(
    "LessonProgress",
    back_populates="user",
    cascade="all, delete-orphan",
    )

    quiz_attempts = relationship(
    "QuizAttempt",
    back_populates="user",
    cascade="all, delete-orphan",
    )

    course_progress = relationship(
    "CourseProgress",
    back_populates="user",
    cascade="all, delete-orphan",
    )

    achievements = relationship(
    "UserAchievement",
    back_populates="user",
    cascade="all, delete-orphan",
    )

    xp_history = relationship(
    "XPHistory",
    back_populates="user",
    cascade="all, delete-orphan",
    )

    coin_history = relationship(
    "CoinHistory",
    back_populates="user",
    cascade="all, delete-orphan",
    )

    missions = relationship(
    "UserMission",
    back_populates="user",
    cascade="all, delete-orphan",
    )

    

