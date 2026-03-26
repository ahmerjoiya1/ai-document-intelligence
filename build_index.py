from app.services.pdf_loader import extract_text_from_pdf   # apna function naam check kar lena
from app.services.text_processor import structure_text_by_page, chunk_text
from app.services.embedding_service import generate_embeddings
from app.services.vector_store import FAISSVectorStore


def main():
    pdf_path = "sample.pdf"

    pages = extract_text_from_pdf(pdf_path)

    # 3. Chunking with metadata
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

    # 4. Extract texts
    texts = [chunk["text"] for chunk in all_chunks]

    # 5. Generate embeddings
    embeddings = generate_embeddings(texts)

    # 6. Create FAISS index
    store = FAISSVectorStore(
        index_path="app/data/faiss/index.bin",
        metadata_path="app/data/faiss/meta.pkl"
    )

    store.create_index(embeddings, all_chunks)
    store.save()

    print("✅ Index created successfully")
    print("Total chunks:", len(all_chunks))


if __name__ == "__main__":
    main()