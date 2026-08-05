from sqlalchemy.orm import Session

from app.models.user import User
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt


def get_dashboard(
    db: Session,
    user: User,
):
    # -------------------------
    # Quiz statistics
    # -------------------------

    attempts = (
        db.query(QuizAttempt)
        .filter(
            QuizAttempt.user_id == user.id
        )
        .all()
    )

    total_attempts = len(attempts)

    if total_attempts > 0:

        average_score = round(
            sum(a.percentage for a in attempts)
            / total_attempts
        )

        passed_attempts = sum(
            1 for a in attempts if a.passed
        )

        pass_rate = round(
            (passed_attempts / total_attempts) * 100
        )

        last_attempt = max(
            attempts,
            key=lambda x: x.submitted_at
        )

        last_quiz_score = last_attempt.percentage

    else:

        average_score = 0
        pass_rate = 0
        last_quiz_score = None
        passed_attempts = 0

    # -------------------------
    # Platform statistics
    # -------------------------

    total_lessons = db.query(Lesson).count()
    total_quizzes = db.query(Quiz).count()

    # -------------------------
    # XP calculations
    # -------------------------

    current_level_xp = (user.level - 1) * 100
    next_level_xp = user.level * 100

    xp_into_level = user.xp - current_level_xp
    xp_remaining = next_level_xp - user.xp

    # -------------------------
    # Dashboard response
    # -------------------------

    return {
        "full_name": user.full_name,
        "level": user.level,
        "xp": user.xp,
        "xp_into_level": xp_into_level,
        "xp_remaining": xp_remaining,
        "xp_to_next_level": xp_remaining,

        "coins": user.coins,
        "streak": user.streak,

        "completed_lessons": user.completed_lessons,
        "completed_quizzes": passed_attempts,

        "total_lessons": total_lessons,
        "total_quizzes": total_quizzes,

        "total_quiz_attempts": total_attempts,
        "average_score": average_score,
        "pass_rate": pass_rate,
        "last_quiz_score": last_quiz_score,

        "current_rank": "Beginner",
    }