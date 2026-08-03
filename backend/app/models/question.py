from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    quiz_id: Mapped[int] = mapped_column(
        ForeignKey("quizzes.id")
    )

    question_text: Mapped[str] = mapped_column(
        Text
    )

    question_order: Mapped[int] = mapped_column(
        Integer
    )

    marks: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    quiz = relationship(
        "Quiz",
        back_populates="questions",
    )

    options = relationship(
        "QuestionOption",
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="QuestionOption.option_order",
    )