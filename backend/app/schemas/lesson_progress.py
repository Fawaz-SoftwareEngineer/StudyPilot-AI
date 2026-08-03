from datetime import datetime

from pydantic import BaseModel


class LessonProgressResponse(BaseModel):
    lesson_id: int
    completed: bool
    completed_at: datetime | None

    model_config = {
        "from_attributes": True,
    }