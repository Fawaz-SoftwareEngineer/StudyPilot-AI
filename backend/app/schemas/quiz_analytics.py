from pydantic import BaseModel


class QuizAnalyticsResponse(BaseModel):
    total_attempts: int
    quizzes_passed: int
    quizzes_failed: int

    best_percentage: int
    average_percentage: float

    total_xp_earned: int
    total_coins_earned: int