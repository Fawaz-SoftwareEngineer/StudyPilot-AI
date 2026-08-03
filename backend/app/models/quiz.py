from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(primary_key=True)

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id"),
        unique=True,
    )

    title: Mapped[str] = mapped_column(
        String(200)
    )

    description: Mapped[str] = mapped_column(
        String(500),
        default="",
    )

    xp_reward: Mapped[int] = mapped_column(
        Integer,
        default=50,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    lesson = relationship(
        "Lesson",
        back_populates="quiz",
    )

    questions = relationship(
        "Question",
        back_populates="quiz",
        cascade="all, delete-orphan",
    )

    attempts = relationship(
        "QuizAttempt",
        back_populates="quiz",
        cascade="all, delete-orphan",
    )