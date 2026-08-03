from app.core.database import Base, engine

# Import models so SQLAlchemy knows about them
from app.models.user import User  # noqa: F401

from app.models.course import Course
from app.models.lesson import Lesson

from app.models.quiz import Quiz

from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.quiz_attempt import QuizAttempt

def init_db():
    Base.metadata.create_all(bind=engine)