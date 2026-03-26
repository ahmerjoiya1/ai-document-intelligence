from fastapi import FastAPI, UploadFile, File
import shutil
import os
from app.services.text_processor import chunk_text
from app.services.embedding_service import generate_embeddings

from app.config import settings
from app.services.pdf_loader import extract_text_from_pdf

app = FastAPI(title=settings.APP_NAME)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "AI Document Intelligence System is running"}


@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.APP_ENV}

@app.post("/upload-pdf/")
def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    data = extract_text_from_pdf(file_path)

    all_chunks = []
    for page in data:
        chunks = chunk_text(page["text"])
        all_chunks.extend(chunks)

    embeddings = generate_embeddings(all_chunks)

    return {
        "filename": file.filename,
        "total_pages": len(data),
        "total_chunks": len(all_chunks),
        "total_embeddings": len(embeddings),
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "first_chunk": all_chunks[0] if all_chunks else "",
        "first_embedding_sample": embeddings[0][:10] if embeddings else []
    }