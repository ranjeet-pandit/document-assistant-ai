"""
Generates embeddings.
"""

from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def generate_embeddings(
        self,
        chunks
    ):

        return self.model.encode(
            chunks
        )