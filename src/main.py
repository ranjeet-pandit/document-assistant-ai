from config import DOCUMENTS_PATH

from services.document_loader import (
    DocumentLoader
)

from services.text_splitter import (
    TextSplitter
)

from services.embedding_service import (
    EmbeddingService
)

from services.vector_store import VectorStore
from services.rag_engine import RAGEngine

loader = DocumentLoader()

documents = loader.load_documents(
    DOCUMENTS_PATH
)

splitter = TextSplitter()

for document in documents:

    print(
        f"\nProcessing: "
        f"{document['filename']}"
    )

    chunks = splitter.split_text(
        document["content"]
    )

    # for index, chunk in enumerate(chunks):

    #     print(
    #         f"\nChunk {index + 1}"
    #     )

    #     print(chunk)

embedding_service = EmbeddingService()

embeddings = embedding_service.generate_embeddings(
    chunks
)

vector_store = VectorStore()

vector_store.store_chunks(
    chunks,
    embeddings
)

# print(
#     f"Generated "
#     f"{len(embeddings)} embeddings"
# )

# print(
#     f"Embedding dimension: "
#     f"{len(embeddings[0])}"
# )

query = "Who approves finance access?"

query_embedding = embedding_service.generate_embeddings(
    [query]
)[0]

results = vector_store.search(
    query_embedding
)

rag_engine = RAGEngine()
context = "\n".join(results)

answer = rag_engine.answer_question(
    query,
    context
)

print("\nAnswer:\n")
print(answer)

# print("\nSearch Results:\n")

# for result in results:
#     print(result)