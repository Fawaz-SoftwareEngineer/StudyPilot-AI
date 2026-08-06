from datetime import datetime

from pydantic import BaseModel


class CoinHistoryResponse(BaseModel):
    id: int
    amount: int
    reason: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }