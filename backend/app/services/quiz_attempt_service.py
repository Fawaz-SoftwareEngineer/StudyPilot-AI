from datetime import datetime

from sqlalchemy.orm import Session

from app.models.lesson_progress import LessonProgress
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.models.user import User

from app.schemas.quiz_attempt import QuizSubmission, QuizResult

from app.services.course_progress_service import update_course_progress

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

    if passed and first_pass is None:

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
        submitted_at=datetime.utcnow(),
    )

    db.add(attempt)

    # ---------------------------------
    # Reward user
    # ---------------------------------

    if xp_gained > 0:

        current_user.xp += xp_gained
        current_user.coins += coins_gained

        current_user.level = (
            current_user.xp // 100
        ) + 1

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
                completed_at=datetime.utcnow(),
            )

            db.add(progress)

            current_user.completed_lessons += 1

            update_course_progress(
            db=db,
            user_id=current_user.id,
            course_id=quiz.lesson.module.course_id,
            )

    db.commit()

    db.refresh(attempt)
    db.refresh(current_user)

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