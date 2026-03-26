from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def generate_embeddings(chunks: list[str]):
    if not chunks:
        return []

    model = get_model()
    embeddings = model.encode(chunks, convert_to_numpy=True)
    return embeddings.tolist()


def generate_query_embedding(query: str):
    if not query or not query.strip():
        return []

    model = get_model()
    embedding = model.encode([query], convert_to_numpy=True)[0]
    return embedding.tolist()