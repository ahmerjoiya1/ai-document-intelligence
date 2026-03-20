from app.services.pdf_loader import extract_text_from_pdf

text = extract_text_from_pdf("sample.pdf")

print("PDF text extracted successfully:\n")
print(text[:2000])