from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    module_id: Mapped[int] = mapped_column(
        ForeignKey("modules.id", ondelete="CASCADE")
    )

    title: Mapped[str] = mapped_column(
        String(200)
    )

    content: Mapped[str] = mapped_column(
        Text
    )

    lesson_order: Mapped[int] = mapped_column(
        Integer
    )

    xp_reward: Mapped[int] = mapped_column(
        Integer,
        default=25,
    )

    # Relationship to Module
    module = relationship(
        "Module",
        back_populates="lessons",
    )

    # Student progress
    progress = relationship(
        "LessonProgress",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )

    # One lesson → One quiz
    quiz = relationship(
        "Quiz",
        back_populates="lesson",
        uselist=False,
        cascade="all, delete-orphan",
    )