from app.services.pdf_loader import extract_text_from_pdf

data = extract_text_from_pdf("sample.pdf")

print("Structured output:\n")

for page_data in data:
    print(page_data)
    print("-" * 80)