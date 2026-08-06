from pydantic import BaseModel


class QuestionReview(BaseModel):
    question_id: int
    question: str

    selected_option: str | None
    correct_option: str

    correct: bool
    marks_awarded: int


class QuizReview(BaseModel):
    quiz_title: str

    score: int
    total_marks: int

    percentage: int
    passed: bool

    questions: list[QuestionReview]