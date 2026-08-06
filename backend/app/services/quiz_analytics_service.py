from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.quiz_attempt import QuizAttempt
from app.models.user import User

from app.schemas.quiz_analytics import QuizAnalyticsResponse


def get_quiz_analytics(
    db: Session,
    current_user: User,
) -> QuizAnalyticsResponse:
    """
    Returns quiz statistics for the logged-in user.
    """

    total_attempts = (
        db.query(func.count(QuizAttempt.id))
        .filter(
            QuizAttempt.user_id == current_user.id
        )
        .scalar()
    ) or 0

    quizzes_passed = (
        db.query(func.count(QuizAttempt.id))
        .filter(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.passed == True,
        )
        .scalar()
    ) or 0

    quizzes_failed = total_attempts - quizzes_passed

    best_percentage = (
        db.query(func.max(QuizAttempt.percentage))
        .filter(
            QuizAttempt.user_id == current_user.id
        )
        .scalar()
    ) or 0

    average_percentage = (
        db.query(func.avg(QuizAttempt.percentage))
        .filter(
            QuizAttempt.user_id == current_user.id
        )
        .scalar()
    ) or 0

    average_percentage = round(
        float(average_percentage),
        2,
    )

    total_xp_earned = (
        db.query(func.sum(QuizAttempt.xp_earned))
        .filter(
            QuizAttempt.user_id == current_user.id
        )
        .scalar()
    ) or 0

    total_coins_earned = (
        db.query(func.sum(QuizAttempt.coins_earned))
        .filter(
            QuizAttempt.user_id == current_user.id
        )
        .scalar()
    ) or 0

    return QuizAnalyticsResponse(
        total_attempts=total_attempts,
        quizzes_passed=quizzes_passed,
        quizzes_failed=quizzes_failed,
        best_percentage=best_percentage,
        average_percentage=average_percentage,
        total_xp_earned=total_xp_earned,
        total_coins_earned=total_coins_earned,
    )