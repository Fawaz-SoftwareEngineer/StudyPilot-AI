from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.database.init_db import init_db

app = FastAPI(
    title="StudyPilot AI",
    version="0.1.0",
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to StudyPilot AI 🚀"
    }