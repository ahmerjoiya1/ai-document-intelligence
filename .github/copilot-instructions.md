# AI Document Intelligence System: Copilot Instructions

## Overview
This repository implements a document processing and Q&A system using FastAPI. The system is designed to evolve into a Retrieval-Augmented Generation (RAG) pipeline. Key components include:

- **Backend**: FastAPI-based API for document processing.
- **Services**: Modular services for PDF loading, text processing, and chunking.
- **Data Flow**: Uploaded PDFs are processed into structured text chunks, enabling downstream AI tasks.

## Key Files and Directories
- `app/main.py`: Entry point for the FastAPI application.
- `app/services/pdf_loader.py`: Handles PDF file loading and text extraction.
- `app/services/text_processor.py`: Cleans, normalizes, and chunks text for AI processing.
- `data/sample_docs/`: Contains example documents for testing.
- `tests/`: Directory for unit and integration tests.

## Developer Workflows
### Running the Application
To start the FastAPI server locally:
```bash
uvicorn app.main:app --reload
```

### Testing
Tests are located in the `tests/` directory. Use the following command to run all tests:
```bash
pytest
```

### Debugging
- Use FastAPI's interactive Swagger UI at `http://127.0.0.1:8000/docs` for API exploration.
- Logs are printed to the console for real-time debugging.

## Project-Specific Conventions
- **Chunking Strategy**: Text is chunked with overlapping segments to preserve context for AI tasks. See `text_processor.py` for implementation details.
- **API Design**: Follow RESTful principles. Each service is modular and encapsulated.
- **File Organization**: Services are grouped by functionality under `app/services/`.

## External Dependencies
- **FastAPI**: For building the backend API.
- **PyPDF2**: For PDF text extraction.
- **pytest**: For testing.

Ensure all dependencies are installed via `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Integration Points
- **PDF Upload**: Endpoint for uploading and processing PDFs.
- **Text Processing**: Service for cleaning and chunking text.

## Examples
### Uploading a PDF
Use the `/upload` endpoint to upload a PDF. Example payload:
```json
{
  "file": "sample.pdf"
}
```

### Extracted Text
Processed text is returned as structured JSON with page-wise and chunked data.

---

This guide is a living document. Update it as the project evolves.