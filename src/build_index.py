from config import DOCUMENTS_PATH

from services.document_loader import DocumentLoader
from services.text_splitter import TextSplitter
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore


loader = DocumentLoader()
splitter = TextSplitter()
embedding_service = EmbeddingService()
vector_store = VectorStore()

documents = loader.load_documents(
    DOCUMENTS_PATH
)

for document in documents:
    print(
        f"\nProcessing: "
        f"{document['filename']}"
    )
    chunks = splitter.split_text(
        document["content"]
    )

    print(
        f"Generated "
        f"{len(chunks)} chunks"
    )

    embeddings = (
        embedding_service
        .generate_embeddings(chunks)
    )

    print(
        f"Generated "
        f"{len(embeddings)} embeddings"
    )

    vector_store.store_chunks(
        chunks,
        embeddings
    )

print("Index built successfully.")