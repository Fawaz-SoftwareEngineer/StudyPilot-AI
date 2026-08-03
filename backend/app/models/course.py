from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(200))

    description: Mapped[str] = mapped_column(String(1000))

    subject: Mapped[str] = mapped_column(String(100))

    difficulty: Mapped[str] = mapped_column(String(50))

    thumbnail: Mapped[str] = mapped_column(
        String(500),
        default="",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    modules = relationship(
    "Module",
    back_populates="course",
    cascade="all, delete-orphan",
    )

    lessons = relationship(
    "Lesson",
    back_populates="course",
    cascade="all, delete-orphan",
    order_by="Lesson.lesson_order",
    )