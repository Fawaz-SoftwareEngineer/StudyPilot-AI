from datetime import datetime

from pydantic import BaseModel


class MissionCreate(BaseModel):
    title: str
    description: str
    mission_type: str
    target_value: int
    xp_reward: int
    coin_reward: int
    is_daily: bool = False
    is_weekly: bool = False


class MissionResponse(BaseModel):
    id: int
    title: str
    description: str
    mission_type: str
    target_value: int
    xp_reward: int
    coin_reward: int
    is_daily: bool
    is_weekly: bool
    is_active: bool

    model_config = {
        "from_attributes": True
    }


class UserMissionResponse(BaseModel):
    id: int
    mission_id: int
    title: str
    description: str
    mission_type: str
    target_value: int

    current_progress: int

    completed: bool
    claimed: bool

    xp_reward: int
    coin_reward: int

    expires_at: datetime

    model_config = {
        "from_attributes": True
    }