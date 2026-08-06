from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    quiz_id: Mapped[int] = mapped_column(
        ForeignKey("quizzes.id", ondelete="CASCADE")
    )

    attempt_number: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    time_taken_seconds: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    total_questions: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    percentage: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    xp_earned: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    coins_earned: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    passed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    user = relationship(
        "User",
        back_populates="quiz_attempts",
    )

    quiz = relationship(
        "Quiz",
        back_populates="attempts",
    )

    answers = relationship(
    "QuizAttemptAnswer",
    back_populates="quiz_attempt",
    cascade="all, delete-orphan",
    )