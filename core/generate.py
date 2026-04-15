import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from core.config import GEN_MODEL, MAX_CONTEXT_CHARS

tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(GEN_MODEL)


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text


def generate_answer(query: str, docs) -> str:
    is_summary = any(x in query.lower() for x in ["overall", "about", "purpose", "summary"])

    context_parts = []
    for doc in docs[:3]:
        text = getattr(doc, "page_content", "")
        text = _clean_text(text)
        context_parts.append(text[:MAX_CONTEXT_CHARS])

    context = "\n\n".join(context_parts)

    if is_summary:
        prompt = f"""
You are a helpful assistant.

Describe the overall purpose of the document in simple English.

Rules:
- One short sentence
- No legal jargon
- No numbers or percentages
- Be general, not clause-specific

Context:
{context}

Answer:
""".strip()
    else:
        prompt = f"""
You are a helpful assistant.

Answer the question using only the context below.

Rules:
- 1 to 2 short sentences
- Use simple English
- Do not copy long legal text
- If unclear, say "The document does not state this clearly."

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
        max_new_tokens=60
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = _clean_text(answer)

    if not answer or len(answer.split()) < 3:
        return "This document defines terms and responsibilities between the involved parties."

    return answer