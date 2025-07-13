import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(
        self,
        index_path="./faiss_index/index.faiss",
        id_map_path="./faiss_index/id_map.npy",
    ):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embedding_size = 384
        self.index_path = index_path
        self.id_map_path = id_map_path

        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

        # Load or initialize FAISS index
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            self.id_map = np.load(self.id_map_path, allow_pickle=True).item()
        else:
            self.index = faiss.IndexFlatL2(self.embedding_size)
            self.id_map = {}

    def embed_text(self, text):
        embedding = self.model.encode([text])
        return np.array(embedding).astype("float32")

    def save(self):
        faiss.write_index(self.index, self.index_path)
        np.save(self.id_map_path, self.id_map)

    def add(self, db_id, text):
        embedding = self.embed_text(text)
        self.index.add(embedding)
        self.id_map[self.index.ntotal - 1] = db_id
        self.save()

    def search(self, query, top_k=3):
        embedding = self.embed_text(query)
        distances, indices = self.index.search(embedding, top_k)
        results = []
        for idx in indices[0]:
            if idx in self.id_map:
                results.append(self.id_map[idx])
        return results
