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
---
## How It Works

```bash
PDF → Text Extraction → Chunking → Embeddings → FAISS Index → Semantic Search → Answer Generation

## Run Locally

```bash
uvicorn app.main:app --reload