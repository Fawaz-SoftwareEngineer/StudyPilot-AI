from sqlalchemy.orm import Session

from app.models.quiz_attempt import QuizAttempt
from app.models.quiz_attempt_answer import QuizAttemptAnswer
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.user import User

from app.schemas.quiz_review import (
    QuizReview,
    QuestionReview,
)


def get_quiz_review(
    db: Session,
    current_user: User,
    attempt_id: int,
) -> QuizReview:
    """
    Returns a complete review of a quiz attempt.
    """

    # ---------------------------------
    # Find quiz attempt
    # ---------------------------------

    attempt = (
        db.query(QuizAttempt)
        .filter(
            QuizAttempt.id == attempt_id,
            QuizAttempt.user_id == current_user.id,
        )
        .first()
    )

    if attempt is None:
        raise ValueError("Quiz attempt not found")

    # ---------------------------------
    # Load submitted answers
    # ---------------------------------

    answers = (
        db.query(QuizAttemptAnswer)
        .filter(
            QuizAttemptAnswer.quiz_attempt_id == attempt.id
        )
        .order_by(
            QuizAttemptAnswer.question_id
        )
        .all()
    )

    question_reviews = []

    # ---------------------------------
    # Build review
    # ---------------------------------

    for answer in answers:

        question = (
            db.query(Question)
            .filter(
                Question.id == answer.question_id
            )
            .first()
        )

        if question is None:
            continue

        selected_option = None

        if answer.selected_option_id is not None:

            option = (
                db.query(QuestionOption)
                .filter(
                    QuestionOption.id == answer.selected_option_id
                )
                .first()
            )

            if option:
                selected_option = option.option_text

        correct_option = (
            db.query(QuestionOption)
            .filter(
                QuestionOption.question_id == question.id,
                QuestionOption.is_correct == True,
            )
            .first()
        )

        question_reviews.append(

            QuestionReview(
                question_id=question.id,
                question=question.question_text,
                selected_option=(
                    selected_option
                ),
                correct_option=(
                    correct_option.option_text
                    if correct_option
                    else ""
                ),
                correct=answer.is_correct,
                marks_awarded=answer.marks_awarded,
            )

        )

    # ---------------------------------
    # Return review
    # ---------------------------------

    return QuizReview(
        quiz_title=attempt.quiz.title,
        score=attempt.score,
        total_marks=attempt.total_questions,
        percentage=attempt.percentage,
        passed=attempt.passed,
        questions=question_reviews,
    )