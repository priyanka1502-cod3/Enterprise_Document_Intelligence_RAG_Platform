# 🤖 Universal Document RAG Assistant

A production-ready Retrieval-Augmented Generation (RAG) system that allows users to upload documents and interact with them using natural language queries.

---

## 🚀 Features

* 📄 Upload PDF/TXT documents
* 🔍 Semantic search using FAISS vector store
* 🧠 LLM-powered question answering
* ⚡ FastAPI backend for scalable APIs
* 💬 ChatGPT-like interface using Gradio
* 📚 Source-based answers (with citations)

---

## 🏗️ Architecture

1. Document ingestion → chunking
2. Embeddings generation (MiniLM)
3. Vector storage (FAISS)
4. Query → semantic retrieval
5. LLM → answer generation

---

## 🛠️ Tech Stack

* Python
* FastAPI
* LangChain
* FAISS
* HuggingFace Transformers
* Gradio

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python -m uvicorn api.main:app --reload
python app.py
```

---

## 📌 Example Use Cases

* Legal document analysis
* Resume screening
* Financial report Q&A
* Enterprise knowledge assistants

---
## 🔥 Key Highlights

- Built a production-ready RAG pipeline from scratch
- Designed modular architecture (API + Core services)
- Implemented semantic search using FAISS
- Integrated LLM for context-aware answer generation
- Created ChatGPT-like UI using Gradio
---
## 💡 Future Improvements

* Authentication
* Multi-user support
* Streaming responses
* Cloud deployment (AWS/GCP)

---

## 👩‍💻 Author

Priyanka
