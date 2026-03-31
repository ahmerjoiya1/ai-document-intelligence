from app.services.embedding_service import generate_query_embedding
from app.services.vector_store import FAISSVectorStore


INDEX_PATH = "app/data/faiss/index.bin"
METADATA_PATH = "app/data/faiss/meta.pkl"


def retrieve_relevant_chunks(query: str, top_k: int = 3):
    query_embedding = generate_query_embedding(query)

    store = FAISSVectorStore(
        index_path=INDEX_PATH,
        metadata_path=METADATA_PATH
    )
    store.load()

    return store.search(query_embedding, top_k=top_k)