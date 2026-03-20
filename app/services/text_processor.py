import re


def clean_text(text: str) -> str:
    if not text:
        return ""

    # Ligature fixes
    text = text.replace("ﬁ", "fi")
    text = text.replace("ﬀ", "ff")
    text = text.replace("ﬂ", "fl")
    text = text.replace("ﬃ", "ffi")
    text = text.replace("ﬄ", "ffl")
    

    # Remove excessive spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Strip each line
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(lines)

    return text.strip()


def structure_text_by_page(reader, filename: str):
    structured_data = []

    for i, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        cleaned_text = clean_text(page_text)

        structured_data.append(
            {
                "page": i + 1,
                "text": cleaned_text,
                "source": filename
            }
        )

    return structured_data