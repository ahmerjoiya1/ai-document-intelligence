from pypdf import PdfReader
from app.services.text_processor import structure_text_by_page


def extract_text_from_pdf(file_path: str):
    reader = PdfReader(file_path)
    structured_data = structure_text_by_page(reader, file_path)
    return structured_data