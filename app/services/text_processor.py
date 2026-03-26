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


def split_into_sentences(text: str):
    return re.split(r"(?<=[.!?])\s+|\n+", text)


def chunk_text(
    text: str,
    chunk_size: int = 300,
    overlap_words: int = 10,
    source: str = "unknown.pdf",
    page: int | None = None,
    start_chunk_id: int = 0,
):
    text = clean_text(text)
    sentences = split_into_sentences(text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if len(current_chunk) + len(sentence) + 1 <= chunk_size:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    overlapped_chunks = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            overlapped_chunks.append(chunk)
        else:
            prev_words = chunks[i - 1].split()
            overlap_text = " ".join(prev_words[-overlap_words:])
            overlapped_chunks.append((overlap_text + " " + chunk).strip())

    structured_chunks = []
    for i, chunk in enumerate(overlapped_chunks):
        structured_chunks.append(
            {
                "chunk_id": start_chunk_id + i,
                "text": chunk,
                "source": source,
                "page": page,
            }
        )

    return structured_chunks