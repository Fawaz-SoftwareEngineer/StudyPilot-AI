from fastapi import FastAPI

app = FastAPI(
    title="StudyPilot AI API",
    description="Backend API for StudyPilot AI",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to StudyPilot AI 🚀",
        "status": "running",
        "version": "0.1.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }