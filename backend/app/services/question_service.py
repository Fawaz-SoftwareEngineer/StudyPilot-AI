from sqlalchemy.orm import Session

from app.models.quiz import Quiz
from app.models.question import Question
from app.schemas.question import QuestionCreate


def create_question(
    db: Session,
    question: QuestionCreate,
):
    quiz = (
        db.query(Quiz)
        .filter(Quiz.id == question.quiz_id)
        .first()
    )

    if quiz is None:
        raise ValueError("Quiz not found")

    new_question = Question(
        quiz_id=question.quiz_id,
        question_text=question.question_text,
        question_order=question.question_order,
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question


def get_questions_by_quiz(
    db: Session,
    quiz_id: int,
):
    return (
        db.query(Question)
        .filter(Question.quiz_id == quiz_id)
        .order_by(Question.question_order)
        .all()
    )