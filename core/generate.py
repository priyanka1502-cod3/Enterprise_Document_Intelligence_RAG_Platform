import os
import re
from groq import Groq

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def generate_answer(query: str, docs) -> str:
    context_parts = []

    for i, doc in enumerate(docs[:3], start=1):
        text = _clean_text(getattr(doc, "page_content", ""))
        context_parts.append(f"Source {i}:\n{text[:1200]}")

    context = "\n\n".join(context_parts)

    system_prompt = """
You are an enterprise document intelligence assistant.
Use ONLY the provided context.
Do not hallucinate.
If the answer is not found, say: "I could not find this information in the document."
Write clearly and professionally.
""".strip()

    user_prompt = f"""
Context:
{context}

Question:
{query}

Answer format:
Short Summary:
- ...

Key Points:
- ...
- ...
- ...
""".strip()

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=400,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Groq generation failed: {e}"