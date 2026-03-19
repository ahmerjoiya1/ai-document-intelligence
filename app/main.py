from fastapi import FastAPI
from app.config import settings

app = FastAPI(title=settings.APP_NAME)


@app.get("/")
def root():
    return {"message": "AI Document Intelligence System is running"}


@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.APP_ENV}