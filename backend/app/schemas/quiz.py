from pydantic import BaseModel


class QuizCreate(BaseModel):
    lesson_id: int
    title: str
    description: str
    passing_score: int = 70
    xp_reward: int = 50
    coins_reward: int = 20


class QuizResponse(BaseModel):
    id: int
    lesson_id: int
    title: str
    description: str
    passing_score: int
    xp_reward: int
    coins_reward: int

    class Config:
        from_attributes = True