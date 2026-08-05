from pydantic import BaseModel


class QuizCreate(BaseModel):
    lesson_id: int
    title: str
    description: str = ""
    xp_reward: int = 50
    passing_percentage: int = 70


class QuizResponse(BaseModel):
    id: int
    lesson_id: int
    title: str
    description: str
    xp_reward: int
    passing_percentage: int

    class Config:
        from_attributes = True