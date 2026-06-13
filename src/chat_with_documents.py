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

    query_embedding = embedding_service.generate_embeddings([query])[0]

    # Fixed Indentation here
    results, metadatas = vector_store.search(query_embedding)
    
    # Format context for the LLM
    context = "\n".join(results)

    answer = rag_engine.answer_question(query, context)

    print("\nAnswer:")
    print(answer)
    
    print("\nSources:")
    # Use a set to avoid showing the same page multiple times
    unique_sources = set()
    for meta in metadatas:
        # Using .get() protects your code if a document doesn't have metadata
        filename = meta.get('filename', 'Unknown File')
        page = meta.get('page', 'unknown')
        unique_sources.add(f"- {filename} (Page {page})")
    
    for source in unique_sources:
        print(source)