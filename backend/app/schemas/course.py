from pydantic import BaseModel
from datetime import datetime


class CourseCreate(BaseModel):
    title: str
    description: str
    subject: str
    difficulty: str
    thumbnail: str = ""


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    subject: str
    difficulty: str
    thumbnail: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }