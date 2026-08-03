from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE")
    )

    title: Mapped[str] = mapped_column(
        String(200)
    )

    description: Mapped[str] = mapped_column(
        String(1000),
        default=""
    )

    module_order: Mapped[int] = mapped_column(
        Integer
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    course = relationship(
        "Course",
        back_populates="modules",
    )

    lessons = relationship(
        "Lesson",
        back_populates="module",
        cascade="all, delete-orphan",
    )