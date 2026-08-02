from fastapi import FastAPI

from app.database.init_db import init_db

app = FastAPI(
    title="StudyPilot AI",
    version="0.1.0",
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {
        "message": "Welcome to StudyPilot AI 🚀"
    }