# Document Assistant

A local Retrieval-Augmented Generation (RAG) application built using Python, Ollama, ChromaDB, and Sentence Transformers.

## Features

- Load TXT and PDF documents
- Generate embeddings locally
- Store embeddings in ChromaDB
- Semantic document search
- Question answering using local LLMs
- Fully offline operation

## Architecture

Document
↓
Chunking
↓
Embeddings
↓
ChromaDB
↓
Retrieval
↓
Qwen Model
↓
Answer

## Technologies

- Python
- Ollama
- Qwen2.5:3B
- ChromaDB
- Sentence Transformers
- PyPDF2

## Setup

### Create Virtual Environment

python -m venv venv

### Activate

venv\Scripts\activate

### Install Dependencies

pip install -r requirements.txt

### Build Index

python src/build_index.py

### Run Assistant

python src/chat_with_documents.py

## Example Questions

What is IDM?

What is access review?

Who approves access requests?

## Future Improvements

- Streamlit UI
- Source citations
- Metadata filtering
- Conversation memory
- IAM Knowledge Bot