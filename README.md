# AI Document Intelligence System

A production-style document processing and Q&A system built with FastAPI, evolving into a full Retrieval-Augmented Generation (RAG) pipeline.

---

## Current Status

- Day 1: Project setup (FastAPI backend, environment, API structure)
- Day 2: PDF text extraction pipeline implemented
- Day 3: Structured output with page-wise extraction via API
- Day 4: Text chunking with overlap for AI-ready processing
- Day 5: Text embeddings generation using SentenceTransformers
- Day 6: Vector database integration (FAISS) for semantic search
- Day 7: Semantic search with query embedding and similarity-based retrieval
- Day 8 & 9: Question-answering pipeline with `/ask` endpoint and source attribution
- Day 10: LLM integration using Hugging Face Inference Providers (RAG pipeline)
- Day 11: Response optimization with prompt engineering and clean formatting  
- Day 12: End-to-end testing, validation, and system refinement 
- Day 13: Streamlit frontend UI skeleton created with sidebar upload section and chat input layout 

---

## Features Implemented

- PDF upload via API
- Text extraction from documents
- Text cleaning and normalization
- Chunking of text into smaller segments
- Context-preserving overlap between chunks
- FastAPI backend with interactive Swagger UI
- Embeddings generation for semantic understanding
- Vector database (FAISS) integration  
- Semantic search using similarity matching 
- Query-based document retrieval  
- Question answering using retrieved document context  
- Source attribution (page number + file reference)
- Interactive API testing via Swagger UI
- Fallback mechanism if LLM fails
- Basic Streamlit frontend setup
- Frontend sidebar for PDF upload
- Chat style input interface in UI
- Clean two-panel layout for demo preparation
- Separated backend (FastAPI) and frontend (Streamlit) project structure
---
## How It Works

```bash
PDF → Text Extraction → Chunking → Embeddings → FAISS Index → Semantic Search → Answer Generation

Architecture
Frontend: Streamlit UI
Backend: FastAPI
Retrieval Layer: FAISS + SentenceTransformers
Generation Layer: Hugging Face Inference Providers

▶️ Run Locally
1. Clone the repo
git clone <https://github.com/ahmerjoiya1/ai-document-intelligence>
2. Install dependencies
pip install -r requirements.txt
3. Set Hugging Face Token
export HF_TOKEN=<your_token_here>
4. Run server
uvicorn app.main:app --reload
5. Open Swagger UI
http://127.0.0.1:8000/docs
6. Run Streamlit UI
streamlit run .\frontend\streamlit_app.py