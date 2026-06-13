"""
Enterprise Document Assistant - Streamlit Frontend UI
Provides a web interface for uploading files, chunking, 
indexing into ChromaDB, and chatting with documents via RAG.
"""

import os
import shutil
from pathlib import Path
import streamlit as st

# Import foundational components from the modular RAG backend
from config import DOCUMENTS_PATH
from services.document_loader import DocumentLoader
from services.embedding_service import EmbeddingService
from services.rag_engine import RAGEngine
from services.text_splitter import TextSplitter
from services.vector_store import VectorStore


# ==========================================
# 1. APPLICATION INITIALIZATION & CACHING
# ==========================================

@st.cache_resource
def init_services():
    """
    Initializes RAG engine services once and caches them.
    Prevents heavy machine learning/database clients from re-loading 
    on every Streamlit interface interaction or user keystroke.
    """
    return {
        "loader": DocumentLoader(),
        "splitter": TextSplitter(),
        "embedding": EmbeddingService(),
        "vector_store": VectorStore(),
        "rag": RAGEngine()
    }

# Instantiate global service mapping
services = init_services()

# Configure basic application layouts
st.set_page_config(page_title="Enterprise Document Assistant", layout="wide")
st.title("📄 Enterprise IAM Knowledge Assistant")
st.subheader("Upload documents and query them locally using RAG")


# ==========================================
# 2. USER INTERFACE LAYOUT (TWO COLUMNS)
# ==========================================

# Create a clean, dual-pane execution container
col1, col2 = st.columns([1, 2])


# --- LEFT COLUMN: Document Management & Database Operations ---
with col1:
    st.header("🗂️ Document Management")
    
    # Ensure physical document folder exists locally
    os.makedirs(DOCUMENTS_PATH, exist_ok=True)
    
    # Drag-and-drop file uploader accepting raw text and enterprise PDFs
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files", 
        type=["pdf", "txt"], 
        accept_multiple_files=True
    )
    
    # Execution button for processing the target document staging area
    if st.button("🚀 Process & Index Documents", use_container_width=True):
        if not uploaded_files:
            st.warning("Please upload at least one file first.")
        else:
            with st.spinner("Processing files..."):
                # Stream uploaded web file bytes into our storage directory
                for uploaded_file in uploaded_files:
                    file_path = Path(DOCUMENTS_PATH) / uploaded_file.name
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                # Execution Pipeline Step 1: Parse and load document structure
                documents = services["loader"].load_documents(DOCUMENTS_PATH)
                
                for document in documents:
                    # Pipeline Step 2: Fragment pages into overlapping chunks
                    chunks = services["splitter"].split_text(document["content"])
                    if not chunks:
                        continue
                    
                    # Generate matching operational metadata maps for each text fragment
                    metadata_list = [
                        {"filename": document["filename"], "page": document["page"]}
                        for _ in range(len(chunks))
                    ]
                    
                    # Pipeline Step 3: Compute mathematical text vector mappings
                    embeddings = services["embedding"].generate_embeddings(chunks)
                    
                    # Pipeline Step 4: Persist embeddings, documents, and labels into vector store
                    services["vector_store"].store_chunks(chunks, embeddings, metadata_list)
                    
            st.success("Database indexed successfully! 🎉")

    # Hard reset capability to wipe local vector store schema
    if st.button("🗑️ Clear Vector Database", use_container_width=True):
        if os.path.exists("./chroma_db"):
            shutil.rmtree("./chroma_db")
            st.success("Vector database wiped. Please re-index documents.")
            st.rerun()  # Forces a clean state refresh of the web interface


# --- RIGHT COLUMN: Conversational Query Interface ---
with col2:
    st.header("💬 Chat Interface")
    
    # Initialize Streamlit session state history array if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display persistent conversation record dynamically on redraw
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            # If an assistant message contains citations, render them inside an expander
            if "sources" in msg and msg["sources"]:
                with st.expander("🔍 View Sources"):
                    for src in msg["sources"]:
                        st.caption(src)

    # Active conversation block listening for enter key submission
    if query := st.chat_input("Ask a question about your documents..."):
        # Display raw prompt immediately in the UI container
        with st.chat_message("user"):
            st.markdown(query)
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Initialize automated response generation
        with st.chat_message("assistant"):
            with st.spinner("Analyzing context and generating answer..."):
                try:
                    # RAG Step 1: Embed incoming conversational prompt
                    query_embedding = services["embedding"].generate_embeddings([query])[0]
                    
                    # RAG Step 2: Fetch contextually relevant records using vector distances
                    results, metadatas = services["vector_store"].search(query_embedding)
                    context = "\n".join(results)
                    
                    # RAG Step 3: Pass contextual data and user question into local LLM
                    answer = services["rag"].answer_question(query, context)
                    st.markdown(answer)
                    
                    # Extraction Loop: Normalize metadata outputs to ensure clean file logs
                    unique_sources = set()
                    for meta in metadatas:
                        filename = meta.get('filename', 'Unknown File')
                        page = meta.get('page', 'unknown')
                        unique_sources.add(f"- {filename} (Page {page})")
                    
                    # RAG Step 4: Display citation summaries nicely under response text
                    sources_list = list(unique_sources)
                    if sources_list:
                        with st.expander("🔍 View Sources"):
                            for src in sources_list:
                                st.caption(src)
                                
                    # Commit final response structure into local application session records
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": sources_list
                    })
                    
                except Exception as e:
                    st.error("Could not complete the query. Make sure documents are indexed first.")