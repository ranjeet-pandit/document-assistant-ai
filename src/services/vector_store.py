"""
Stores and retrieves embeddings using ChromaDB.
"""

import chromadb
import uuid
from utils.logger import get_logger

logger = get_logger("services.vector_store")

class VectorStore:
    def __init__(self):
        logger.info("Initializing persistent ChromaDB client connecting to ./chroma_db...")
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name="documents")

    def store_chunks(self, chunks, embeddings, metadata_list):
        logger.info(f"Preparing to commit {len(chunks)} text chunks to ChromaDB...")
        try:
            for index, chunk in enumerate(chunks):
                self.collection.add(
                    ids=[str(uuid.uuid4())],
                    embeddings=[embeddings[index].tolist()],
                    metadatas=[metadata_list[index]],
                    documents=[chunk]
                )
            logger.info("Batch transaction committed to Vector Store successfully. ✅")
        except Exception as e:
            logger.error(f"Failed to commit transaction to ChromaDB: {str(e)}")
            raise e

    def search(self, query_embedding, top_k=3):
        logger.info(f"Executing Vector Semantic Search query (top_k={top_k})...")
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        logger.info(f"Search complete. Retrieved {len(results['documents'][0])} matched document contexts.")
        return results["documents"][0], results["metadatas"][0]
