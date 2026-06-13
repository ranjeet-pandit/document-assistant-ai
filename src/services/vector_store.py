"""
Stores and retrieves embeddings using ChromaDB.
"""

import chromadb

import uuid


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def store_chunks(
        self,
        chunks,
        embeddings
    ):

        for index, chunk in enumerate(chunks):

            self.collection.add(
                ids=[str(uuid.uuid4())],
                embeddings=[embeddings[index].tolist()],
                documents=[chunk]
            )

    def search(
        self,
        query_embedding,
        top_k=2
    ):

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )

        return results["documents"][0]