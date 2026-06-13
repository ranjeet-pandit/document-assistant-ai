from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore
from services.rag_engine import RAGEngine

embedding_service = EmbeddingService()
vector_store = VectorStore()
rag_engine = RAGEngine()

print("Document Assistant")
print("Type 'exit' to quit")

while True:

    query = input("\nQuestion: ")

    if query.lower() == "exit":
        break

    query_embedding = (
        embedding_service
        .generate_embeddings([query])[0]
    )

    results = vector_store.search(
        query_embedding
    )

    context = "\n".join(results)

    answer = rag_engine.answer_question(
        query,
        context
    )

    print("\nAnswer:")
    print(answer)