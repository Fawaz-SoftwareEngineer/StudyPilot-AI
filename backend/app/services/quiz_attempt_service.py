from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.lesson_progress import LessonProgress
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.models.user import User

from app.schemas.quiz_attempt import QuizSubmission, QuizResult

from app.services.course_progress_service import update_course_progress
from app.services.achievement_service import unlock_achievement

from app.models.quiz_attempt_answer import QuizAttemptAnswer

from app.services.coin_history_service import add_coin_history

COINS_PER_QUIZ = 20


def submit_quiz(
    db: Session,
    current_user: User,
    submission: QuizSubmission,
) -> QuizResult:

    # ---------------------------------
    # Find quiz
    # ---------------------------------

    quiz = (
        db.query(Quiz)
        .filter(Quiz.id == submission.quiz_id)
        .first()
    )

    if quiz is None:
        raise ValueError("Quiz not found")

    # ---------------------------------
    # Load active questions
    # ---------------------------------

    questions = (
        db.query(Question)
        .filter(
            Question.quiz_id == quiz.id,
            Question.is_active == True,
        )
        .order_by(Question.question_order)
        .all()
    )

    if not questions:
        raise ValueError("Quiz has no questions")

    total_questions = len(questions)

    # ---------------------------------
    # Submitted answers lookup
    # ---------------------------------

    submitted_answers = {
        answer.question_id: answer.selected_option_id
        for answer in submission.answers
    }

    # ---------------------------------
    # Grade quiz
    # ---------------------------------

    score = 0

    for question in questions:

        correct_option = (
            db.query(QuestionOption)
            .filter(
                QuestionOption.question_id == question.id,
                QuestionOption.is_correct == True,
            )
            .first()
        )

        if correct_option is None:
            continue

        selected_option = submitted_answers.get(question.id)

        if selected_option == correct_option.id:
            score += question.marks

    # ---------------------------------
    # Calculate percentage
    # ---------------------------------

    total_marks = sum(
        question.marks
        for question in questions
    )

    if total_marks == 0:
        percentage = 0
    else:
        percentage = round(
            (score / total_marks) * 100
        )

    passed = (
        percentage >= quiz.passing_percentage
    )

    # ---------------------------------
    # Calculate attempt number
    # ---------------------------------

    attempt_number = (
        db.query(QuizAttempt)
        .filter(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.quiz_id == quiz.id,
        )
        .count()
        + 1
    )

    # ---------------------------------
    # Reward only on first successful pass
    # ---------------------------------

    first_pass = (
        db.query(QuizAttempt)
        .filter(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.quiz_id == quiz.id,
            QuizAttempt.passed == True,
        )
        .first()
    )

    is_first_success = (
    passed
    and first_pass is None
    )

    if is_first_success:
        xp_gained = quiz.xp_reward
        coins_gained = COINS_PER_QUIZ
    else:
        xp_gained = 0
        coins_gained = 0

    # ---------------------------------
    # Save attempt
    # ---------------------------------

    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz.id,
        attempt_number=attempt_number,
        time_taken_seconds=submission.time_taken_seconds,
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        xp_earned=xp_gained,
        coins_earned=coins_gained,
        passed=passed,
        submitted_at=datetime.now(timezone.utc),
    )

    db.add(attempt)
    db.flush()

    # ---------------------------------
    # Save every submitted answer
    # ---------------------------------

    for question in questions:

        selected_option_id = submitted_answers.get(question.id)

        correct_option = (
            db.query(QuestionOption)
            .filter(
            QuestionOption.question_id == question.id,
            QuestionOption.is_correct == True,
        )
        .first()
        )

        is_correct = (
            selected_option_id == correct_option.id
            if correct_option is not None and selected_option_id is not None
            else False
        )

        marks_awarded = (
            question.marks
            if is_correct
            else 0
        )

        answer = QuizAttemptAnswer(
            quiz_attempt_id=attempt.id,
            question_id=question.id,
            selected_option_id=selected_option_id,
            is_correct=is_correct,
            marks_awarded=marks_awarded,
        )

        db.add(answer)

    # ---------------------------------
    # Reward user
    # ---------------------------------

    if xp_gained > 0:

        current_user.xp += xp_gained
        current_user.coins += coins_gained
        
        add_coin_history(
            db=db,
            user=current_user,
            amount=coins_gained,
            reason="Quiz Completion",
        )

        current_user.level = (current_user.xp // 100) + 1

        unlock_achievement(
            db,
            current_user,
            "First Quiz",
        )

        progress = (
            db.query(LessonProgress)
            .filter(
                LessonProgress.user_id == current_user.id,
                LessonProgress.lesson_id == quiz.lesson_id,
            )
            .first()
        )

        if progress is None:

            progress = LessonProgress(
                user_id=current_user.id,
                lesson_id=quiz.lesson_id,
                completed=True,
                completed_at=datetime.now(timezone.utc),
            )

            db.add(progress)

            current_user.completed_lessons += 1

            update_course_progress(
                db=db,
                user_id=current_user.id,
                course_id=quiz.lesson.module.course_id,
            )

    try:
        db.commit()

        db.refresh(attempt)
        db.refresh(current_user)

    except Exception:
        db.rollback()
        raise

    return QuizResult(
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        passed=passed,
        xp_gained=xp_gained,
        coins_gained=coins_gained,
        attempt_number=attempt_number,
        message=(
            "Quiz passed successfully!"
            if passed
            else "Quiz failed. Try again."
    )
)