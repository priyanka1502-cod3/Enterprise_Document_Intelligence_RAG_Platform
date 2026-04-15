from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from core.config import UPLOAD_DIR, TOP_K
from core.ingest import load_documents, split_documents
from core.vectorstore import create_vectorstore
from core.retrieve import search_documents
from core.generate import generate_answer

app = FastAPI(title="Universal Document RAG API")

upload_dir = Path(UPLOAD_DIR)
upload_dir.mkdir(parents=True, exist_ok=True)


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    ext = Path(file.filename).suffix.lower()
    if ext not in [".pdf", ".txt"]:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")

    file_path = upload_dir / file.filename

    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        docs = load_documents(str(file_path))
        chunks = split_documents(docs)
        create_vectorstore(chunks)

        return {
            "message": "File uploaded, processed, and indexed",
            "filename": file.filename,
            "total_chunks": len(chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload/index failed: {e}")


@app.post("/query")
def query_documents(payload: QueryRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        results = search_documents(question, k=TOP_K)
        if not results:
            raise HTTPException(status_code=404, detail="No relevant content found")

        answer = generate_answer(question, results)

        clean_sources = []
        for r in results[:3]:
            clean_sources.append({
                "page": r.metadata.get("page", "N/A"),
                "preview": r.page_content[:180].replace("\n", " ").strip()
            })

        return {
            "question": payload.question,
            "answer": answer,
            "sources": clean_sources
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")