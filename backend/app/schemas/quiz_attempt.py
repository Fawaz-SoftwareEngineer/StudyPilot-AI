from pydantic import BaseModel


class QuizAnswer(BaseModel):
    question_id: int
    selected_option_id: int


class QuizSubmission(BaseModel):
    quiz_id: int
    answers: list[QuizAnswer]
    time_taken_seconds: int = 0


class QuizResult(BaseModel):
    score: int
    total_questions: int
    percentage: int
    passed: bool

    xp_gained: int
    coins_gained: int

    attempt_number: int

    message: str