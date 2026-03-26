import os
import pickle
from typing import List, Dict, Any

import faiss
import numpy as np


class FAISSVectorStore:
    def __init__(self, index_path: str, metadata_path: str):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.index = None
        self.metadata = []

    def create_index(self, embeddings: List[List[float]], metadata: List[Dict[str, Any]]) -> None:
        if not embeddings:
            raise ValueError("Embeddings list is empty.")

        if len(embeddings) != len(metadata):
            raise ValueError("Embeddings and metadata must have the same length.")

        vectors = np.array(embeddings, dtype=np.float32)
        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(vectors)

        self.metadata = metadata

    def save(self) -> None:
        if self.index is None:
            raise ValueError("No FAISS index found to save.")

        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

        faiss.write_index(self.index, self.index_path)

        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self) -> None:
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Index file not found: {self.index_path}")

        if not os.path.exists(self.metadata_path):
            raise FileNotFoundError(f"Metadata file not found: {self.metadata_path}")

        self.index = faiss.read_index(self.index_path)

        with open(self.metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        if self.index is None:
            raise ValueError("FAISS index is not loaded.")

        query_vector = np.array([query_embedding], dtype=np.float32)
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            if idx >= len(self.metadata):
                continue

            results.append({
                "score": float(distance),
                "metadata": self.metadata[idx]
            })

        return results