# 📑 Local Enterprise Document Assistant (RAG)

An enterprise-grade, completely private Retrieval-Augmented Generation (RAG) application. This system allows you to upload unstructured files (PDFs/TXT), index them with sliding-window semantic chunking, store them into a persistent vector database, and query them locally using an open-source Large Language Model (LLM)—complete with auditable page-level source citations.

---

## 🏗️ Architectural Pipeline

```text
[Web UI Framework] ──(Upload Document)──> [Document Loader Service]
        │                                             │
   (User Input Query)                                 ▼
        │                                  [Text Splitting Engine]
        ▼                                 (Sliding-Window Overlaps)
 [Ollama Client]                                      │
        │                                             ▼
   (LLM Brain)                             [Sentence Transformers]
        │                                  (Vector Matrix Encoders)
        ▼                                             │
[Contextual Generation] <──(Search Top_K)─────────────▼
        │                                    [ChromaDB Vector Store]
        ▼
[Auditable Citations]

```

---

## 🛠️ Prerequisites & Dependencies

Before setting up the python workspace, ensure you have the following baseline components configured on your workstation:

* **Python:** `3.10` or higher recommended.
* **Ollama (Local Inference Engine):** [Download Ollama](https://ollama.com/) and verify it is running in your background or tray icon.

Download the required local model files by executing the following instruction in your system terminal:

```powershell
ollama pull qwen2.5:3b

```

---

## 🚀 Ingestion & Execution Setup

Follow these linear procedural steps to spin up the localized application workspace:

1. **Clone the Repository:** Under 1 min.
Pull down the project architecture to your local staging repository workspace:

```powershell
git clone <your-github-repository-url>
cd document-assistant

```


2. **Install Runtime Dependencies:** 2-3 min.
Install the core machine learning libraries, document parsers, database bindings, and frontend framework packages via `pip`:

```powershell
pip install streamlit sentence-transformers chromadb pypdf requests

```


3. **Configure Streamlit Watcher Overrides:** 30 seconds.
Ensure your project root folder contains a `.streamlit/config.toml` layout file with the following explicit blocks to prevent deep-scanning third-party package libraries on Windows systems:

```toml
[server]
fileWatcherType = "none"

[browser]
gatherUsageStats = false

```


4. **Execute the Web Application Interface:** Immediate.
Launch the interactive browser application container by running the main interface initialization module:

```powershell
streamlit run src/app.py

```


---

## 🖥️ Application Core Features

* **Advanced Sliding-Window Chunking:** Utilizes overlapping text windows (600 characters, 100 characters overlap) inside `services/text_splitter.py` to prevent data clipping and retain semantic continuity across block edges.
* **Granular Page Processing:** Documents are loaded page-by-page dynamically, preserving source file names and structural page layouts as explicit dictionary data variables.
* **Auditable Page-Level Metadata:** Ingestion structures link computational embeddings to concrete positional coordinates in the database matrix, returning expandable dropdown references inside the chat window.
* **Completely Private Local Storage:** Persistent vectors map directly onto file directories inside `./chroma_db`, ensuring information stays securely behind your corporate firewall.

---

> 🔒 **Security Note:** This system operates completely offline. Embedding compilation and language generation loops execute entirely within your native processor architecture, ensuring zero data leakage to cloud APIs.