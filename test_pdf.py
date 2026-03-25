from app.services.pdf_loader import extract_text_from_pdf
from app.services.text_processor import chunk_text

data = extract_text_from_pdf("sample.pdf")

print("Chunked output:\n")

for page in data:
    print(f"\n--- PAGE {page['page']} ---")
    chunks = chunk_text(page["text"])

    for i, chunk in enumerate(chunks, start=1):
        print(f"\nChunk {i}:\n{chunk}")
        print("-" * 80)