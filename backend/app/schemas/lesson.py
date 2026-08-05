from pydantic import BaseModel


class LessonCreate(BaseModel):
    module_id: int
    title: str
    content: str
    lesson_order: int
    xp_reward: int = 25


class LessonResponse(BaseModel):
    id: int
    module_id: int
    title: str
    content: str
    lesson_order: int
    xp_reward: int

    class Config:
        from_attributes = True