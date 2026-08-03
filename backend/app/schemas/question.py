from pydantic import BaseModel


class QuestionCreate(BaseModel):
    quiz_id: int
    question_text: str
    question_order: int


class QuestionResponse(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    question_order: int

    class Config:
        from_attributes = True