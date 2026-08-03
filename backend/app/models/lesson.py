from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id")
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

    course = relationship(
        "Course",
        back_populates="lessons",
    )

    progress = relationship(
    "LessonProgress",
    back_populates="lesson",
    cascade="all, delete-orphan",
    )

    quiz = relationship(
    "Quiz",
    back_populates="lesson",
    uselist=False,
    )