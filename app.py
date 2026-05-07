import gradio as gr
from pathlib import Path

from core.ingest import load_documents, split_documents
from core.vectorstore import create_vectorstore
from core.retrieve import search_documents
from core.generate import generate_answer

UPLOAD_DIR = "data/uploads"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


def upload_file(file):
    if file is None:
        return "Please upload a PDF or TXT file."

    file_path = Path(UPLOAD_DIR) / Path(file.name).name

    with open(file.name, "rb") as src:
        with open(file_path, "wb") as dst:
            dst.write(src.read())

    docs = load_documents(str(file_path))
    chunks = split_documents(docs)
    create_vectorstore(chunks)

    return f"Uploaded and indexed successfully. Total chunks: {len(chunks)}"


def answer_question(question):
    if not question.strip():
        return "Please enter a question."

    try:
        results = search_documents(question, k=3)

        if not results:
            return "No relevant content found."

        answer = generate_answer(question, results)

        sources = []
        for doc in results[:3]:
            page = doc.metadata.get("page", "N/A")
            preview = doc.page_content[:180].replace("\n", " ").strip()
            sources.append(f"Source {len(sources)+1} | Page {page}\n{preview}...")

        source_text = "\n".join(sources) if sources else "No sources available."

        return answer + "\n\nSources:\n" + source_text

    except Exception as e:
        return f"Error: {e}"


with gr.Blocks(theme=gr.themes.Soft(), title="Enterprise Document Intelligence RAG Platform") as demo:
    gr.Markdown("# Enterprise Document Intelligence RAG Platform")
    gr.Markdown(
    "Upload a PDF or TXT document and ask questions. "
    "The system uses Retrieval-Augmented Generation with FAISS vector search "
    "and source-grounded answer generation."
     )
    file_input = gr.File(label="Upload PDF or TXT Document")
    upload_status = gr.Textbox(label="Indexing Status", interactive=False)

    upload_btn = gr.Button("Upload & Index")
    upload_btn.click(upload_file, inputs=file_input, outputs=upload_status)

    question = gr.Textbox(
        label="Ask a Question",
        placeholder="Example: Summarize the main purpose of this document."
    )

    answer = gr.Textbox(label="Answer with Sources", lines=12)

    ask_btn = gr.Button("Ask")
    ask_btn.click(answer_question, inputs=question, outputs=answer)


demo.launch()