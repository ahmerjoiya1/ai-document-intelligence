from app.services.pdf_loader import extract_text_from_pdf
from app.services.text_processor import chunk_text
from app.services.embedding_service import generate_embeddings

data = extract_text_from_pdf("sample.pdf")

all_chunks = []

for page in data:
    chunks = chunk_text(page["text"])
    all_chunks.extend(chunks)

print(f"\nTotal chunks: {len(all_chunks)}")

embeddings = generate_embeddings(all_chunks)

print(f"Total embeddings generated: {len(embeddings)}")

if embeddings:
    print(f"Embedding dimension: {len(embeddings[0])}")
    print(f"First chunk:\n{all_chunks[0]}")
    print(f"\nFirst embedding sample (first 10 values):\n{embeddings[0][:10]}")