from fastapi import FastAPI, UploadFile, File
import shutil
import os
from app.services.text_processor import chunk_text

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

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract structured data
    data = extract_text_from_pdf(file_path)

    all_chunks = []

    for page in data:
        chunks = chunk_text(page["text"])
        all_chunks.append({
            "page": page["page"],
            "chunks": chunks
        })

    return {
        "filename": file.filename,
        "total_pages": len(data),
        "preview": data[:1],
        "chunks": all_chunks
    }