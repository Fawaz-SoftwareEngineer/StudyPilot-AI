from datetime import datetime

from pydantic import BaseModel


class AchievementCreate(BaseModel):
    name: str
    description: str
    icon: str = "🏆"
    xp_reward: int = 0
    coins_reward: int = 0


class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    xp_reward: int
    coins_reward: int

    class Config:
        from_attributes = True


class UserAchievementResponse(BaseModel):
    id: int
    unlocked_at: datetime
    achievement: AchievementResponse

    class Config:
        from_attributes = True