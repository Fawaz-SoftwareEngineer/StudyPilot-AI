from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.database.init_db import init_db

from app.api.dashboard import router as dashboard_router

from app.api.progress import router as progress_router

from app.api.course import router as course_router

from app.api.quiz import router as quiz_router

from app.api.question import router as question_router

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

@app.get("/")
def root():
    return {
        "message": "Welcome to StudyPilot AI 🚀"
    }