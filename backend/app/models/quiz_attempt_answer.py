from sqlalchemy import Boolean, ForeignKey, Integer

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


class QuizAttemptAnswer(Base):
    __tablename__ = "quiz_attempt_answers"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    quiz_attempt_id: Mapped[int] = mapped_column(
        ForeignKey(
            "quiz_attempts.id",
            ondelete="CASCADE",
        )
    )

    question_id: Mapped[int] = mapped_column(
        ForeignKey(
            "questions.id",
            ondelete="CASCADE",
        )
    )

    selected_option_id: Mapped[int] = mapped_column(
        ForeignKey(
            "question_options.id",
            ondelete="CASCADE",
        )
    )

    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    marks_awarded: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    quiz_attempt = relationship(
        "QuizAttempt",
        back_populates="answers",
    )

    question = relationship(
        "Question",
    )

    selected_option = relationship(
        "QuestionOption",
    )