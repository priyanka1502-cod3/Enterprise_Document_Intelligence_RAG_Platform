import mimetypes
import requests
import gradio as gr

API_BASE = "http://127.0.0.1:8000"


def upload_file_fn(file):
    if file is None:
        return "Please choose a PDF or TXT file first."

    filename = file.name.split("/")[-1]
    mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    try:
        with open(file.name, "rb") as f:
            files = {"file": (filename, f, mime_type)}
            response = requests.post(f"{API_BASE}/upload", files=files, timeout=300)

        response.raise_for_status()
        data = response.json()
        return f"Uploaded and indexed: {data['filename']} | Total chunks: {data['total_chunks']}"
    except requests.RequestException as e:
        return f"Upload failed: {e}"


def respond(message, history):
    try:
        recent_history = history[-4:] if history else []

        memory_text = ""
        for user_msg, bot_msg in recent_history:
            memory_text += f"User: {user_msg}\nAssistant: {bot_msg}\n"

        final_question = f"""
Conversation history:
{memory_text}

Current question:
{message}
""".strip()

        response = requests.post(
            f"{API_BASE}/query",
            json={"question": final_question},
            timeout=300
        )
        response.raise_for_status()
        data = response.json()

        answer = data.get("answer", "No answer returned.")
        sources = data.get("sources", [])

        source_lines = []
        for src in sources[:2]:
            page = src.get("page", "N/A")
            preview = src.get("preview", "").replace("\n", " ").strip()
            source_lines.append(f"• Page {page}: {preview[:120]}...")

        source_text = "\n".join(source_lines) if source_lines else "No sources available."

        return f"{answer}\n\nSources:\n{source_text}"

    except Exception as e:
        return f"Error: {e}"