from pydantic import BaseModel


class QuestionOptionCreate(BaseModel):
    question_id: int
    option_text: str
    option_order: int
    is_correct: bool = False


class QuestionOptionResponse(BaseModel):
    id: int
    question_id: int
    option_text: str
    option_order: int
    is_correct: bool

    class Config:
        from_attributes = True