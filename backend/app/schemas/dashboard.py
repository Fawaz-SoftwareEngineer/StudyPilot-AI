from pydantic import BaseModel


class DashboardResponse(BaseModel):
    full_name: str
    level: int
    xp: int
    coins: int
    streak: int
    completed_lessons: int