from config import DOCUMENTS_PATH
from services.document_loader import DocumentLoader
from services.text_splitter import TextSplitter
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore

loader = DocumentLoader()
splitter = TextSplitter()
embedding_service = EmbeddingService()
vector_store = VectorStore()

documents = loader.load_documents(DOCUMENTS_PATH)

for document in documents:
    print(f"\nProcessing: {document['filename']} (Page {document['page']})")
    
    # 1. Split the page content into overlapping chunks
    chunks = splitter.split_text(document["content"])
    print(f"Generated {len(chunks)} chunks")

    if not chunks:
        continue

    # 2. Create a metadata dictionary for every chunk generated from this page
    metadata_list = [
        {
            "filename": document["filename"],
            "page": document["page"]
        }
        for _ in range(len(chunks))
    ]

    # 3. Generate embeddings for the chunks
    embeddings = embedding_service.generate_embeddings(chunks)
    print(f"Generated {len(embeddings)} embeddings")

    # 4. Store everything in ChromaDB (now passing the metadata!)
    vector_store.store_chunks(chunks, embeddings, metadata_list)

print("\nIndex built successfully with source tracking! 🎉")