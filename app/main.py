from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os

from app.config import settings
from app.services.pdf_loader import extract_text_from_pdf
from app.services.text_processor import chunk_text
from app.services.embedding_service import generate_embeddings, generate_query_embedding
from app.services.vector_store import FAISSVectorStore
from app.services.retriever import retrieve_relevant_chunks
from app.services.llm_service import generate_answer

app = FastAPI(title=settings.APP_NAME)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# 🔹 Load FAISS (global)
vector_store = FAISSVectorStore(
    index_path="app/data/faiss/index.bin",
    metadata_path="app/data/faiss/meta.pkl"
)

# Agar pehle se index exist karta hai to load karo
try:
    vector_store.load()
except:
    print("⚠️ No existing index found. Upload a PDF first.")


# -----------------------------
# BASIC ROUTES
# -----------------------------

@app.get("/")
def root():
    return {"message": "AI Document Intelligence System is running"}


@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.APP_ENV}


# -----------------------------
# UPLOAD + INDEXING
# -----------------------------

@app.post("/upload-pdf/")
def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract structured text
    pages = extract_text_from_pdf(file_path)

    # Chunking with metadata
    all_chunks = []
    next_chunk_id = 0

    for page in pages:
        page_chunks = chunk_text(
            text=page["text"],
            source=page["source"],
            page=page["page"],
            start_chunk_id=next_chunk_id
        )

        all_chunks.extend(page_chunks)
        next_chunk_id += len(page_chunks)

    # Extract texts
    texts = [chunk["text"] for chunk in all_chunks]

    # Generate embeddings
    embeddings = generate_embeddings(texts)

    # Create & save FAISS index
    vector_store.create_index(embeddings, all_chunks)
    vector_store.save()

    return {
        "filename": file.filename,
        "total_pages": len(pages),
        "total_chunks": len(all_chunks),
        "message": "PDF processed and indexed successfully ✅"
    }


# -----------------------------
# SEARCH (BROWSER FRIENDLY)
# -----------------------------

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

class AskRequest(BaseModel):
    query: str
    top_k: int = 3

@app.post("/search")
def search(request: SearchRequest):
    query_embedding = generate_query_embedding(request.query)

    results = vector_store.search(query_embedding, request.top_k)

    return {
        "query": request.query,
        "results": results
    }

@app.post("/ask")
def ask(request: AskRequest):
    try:
        retrieved_results = retrieve_relevant_chunks(
            query=request.query,
            top_k=request.top_k
        )

        response = generate_answer(
            query=request.query,
            retrieved_results=retrieved_results
        )

        return {
            "query": request.query,
            "answer": response["answer"],
            "sources": response["sources"]
        }

    except Exception as e:
        return {"error": str(e)}