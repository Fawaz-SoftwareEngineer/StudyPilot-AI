from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.schemas.quiz import QuizCreate


def create_quiz(db: Session, quiz: QuizCreate):

    lesson = (
        db.query(Lesson)
        .filter(Lesson.id == quiz.lesson_id)
        .first()
    )

    if lesson is None:
        raise ValueError("Lesson not found")

    new_quiz = Quiz(
        lesson_id=quiz.lesson_id,
        title=quiz.title,
        description=quiz.description,
        passing_score=quiz.passing_score,
        xp_reward=quiz.xp_reward,
        coins_reward=quiz.coins_reward,
    )

    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    return new_quiz


def get_all_quizzes(db: Session):
    return db.query(Quiz).all()


def get_quiz(db: Session, quiz_id: int):
    return (
        db.query(Quiz)
        .filter(Quiz.id == quiz_id)
        .first()
    )