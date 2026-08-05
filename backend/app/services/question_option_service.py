from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.question_option import QuestionOption
from app.schemas.question_option import QuestionOptionCreate


def create_option(
    db: Session,
    option: QuestionOptionCreate,
):
    question = (
        db.query(Question)
        .filter(Question.id == option.question_id)
        .first()
    )

    if question is None:
        raise ValueError("Question not found")

    new_option = QuestionOption(
        question_id=option.question_id,
        option_text=option.option_text,
        option_order=option.option_order,
        is_correct=option.is_correct,
    )

    db.add(new_option)
    db.commit()
    db.refresh(new_option)

    return new_option


def get_question_options(
    db: Session,
    question_id: int,
):
    return (
        db.query(QuestionOption)
        .filter(
            QuestionOption.question_id == question_id
        )
        .order_by(
            QuestionOption.option_order
        )
        .all()
    )