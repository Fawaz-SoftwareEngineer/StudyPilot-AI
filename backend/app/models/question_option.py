from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class QuestionOption(Base):
    __tablename__ = "question_options"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id")
    )

    option_text: Mapped[str] = mapped_column(
        String(500)
    )

    option_order: Mapped[int] = mapped_column(
        Integer
    )

    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    question = relationship(
        "Question",
        back_populates="options",
    )