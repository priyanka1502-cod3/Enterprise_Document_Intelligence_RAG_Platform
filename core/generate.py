import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from core.config import GEN_MODEL, MAX_CONTEXT_CHARS

tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(GEN_MODEL)


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text


def generate_answer(query: str, docs) -> str:
    context_parts = []

    for i, doc in enumerate(docs[:3], start=1):
        text = getattr(doc, "page_content", "")
        text = _clean_text(text)
        context_parts.append(f"Source {i}: {text[:MAX_CONTEXT_CHARS]}")

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an intelligent document assistant.

Answer the user question using only the provided context.

Rules:
- Give a clear and simple answer.
- Keep the answer concise.
- Do not copy long text from the document.
- If the answer is not available in the context, say: "I could not find this information in the document."
- Do not hallucinate.

Context:
{context}

Question:
{query}

Answer:
""".strip()

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=120,
        num_beams=4,
        early_stopping=True
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = _clean_text(answer)

    if not answer or len(answer.split()) < 4:
        return "I could not generate a reliable answer from the retrieved context."

    return answer