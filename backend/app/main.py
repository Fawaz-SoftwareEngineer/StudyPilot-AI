from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.database.init_db import init_db

from app.api.dashboard import router as dashboard_router

from app.api.progress import router as progress_router

from app.api.course import router as course_router

from app.api.quiz import router as quiz_router

from app.api.question import router as question_router

from app.api.lesson import router as lesson_router

from app.api import quiz_attempt

from app.api import module

from app.api import question_option

from app.api.achievement import router as achievement_router

from app.api.quiz_review import router as quiz_review_router

from app.api import quiz_analytics

from app.api import coin_history

from app.api import mission

app = FastAPI(
    title="StudyPilot AI",
    version="0.1.0",
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(progress_router)
app.include_router(course_router)
app.include_router(quiz_router)
app.include_router(question_router)
app.include_router(lesson_router)
app.include_router(question_option.router)
app.include_router(achievement_router)
app.include_router(quiz_review_router)
app.include_router(coin_history.router)
app.include_router(mission.router)

app.include_router(
    quiz_analytics.router
)

app.include_router(
    quiz_attempt.router
)

app.include_router(module.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to StudyPilot AI 🚀"
    }