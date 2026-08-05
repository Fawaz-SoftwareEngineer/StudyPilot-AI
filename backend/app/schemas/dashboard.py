from pydantic import BaseModel


class DashboardResponse(BaseModel):
    full_name: str
    level: int
    xp: int
    coins: int
    streak: int

    completed_lessons: int
    completed_quizzes: int

    total_lessons: int
    total_quizzes: int

    current_rank: str
    xp_to_next_level: int

    class Config:
        from_attributes = True