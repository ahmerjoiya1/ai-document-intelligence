# AI Document Intelligence System

A production-style document processing and Q&A system built with FastAPI, evolving into a full Retrieval-Augmented Generation (RAG) pipeline.

---

## Current Status

- Day 1: Project setup (FastAPI backend, environment, API structure)
- Day 2: PDF text extraction pipeline implemented
- Day 3: Structured output with page-wise extraction via API
- Day 4: Text chunking with overlap for AI-ready processing

---

## Features Implemented

- PDF upload via API
- Text extraction from documents
- Text cleaning and normalization
- Chunking of text into smaller segments
- Context-preserving overlap between chunks
- FastAPI backend with interactive Swagger UI

---

## Run Locally

```bash
uvicorn app.main:app --reload