from typing import List, Dict, Any
import re
import os
from huggingface_hub import InferenceClient

_client = None


def get_client():
    global _client

    if _client is None:
        hf_token = os.getenv("HF_TOKEN")
        print("HF_TOKEN exists:", bool(hf_token))

        if not hf_token:
            return None

        _client = InferenceClient(api_key=hf_token)

    return _client


def clean_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def truncate_text(text: str, max_chars: int = 1000) -> str:
    text = clean_text(text)
    return text[:max_chars]


def build_prompt(query: str, retrieved_results: List[Dict[str, Any]]) -> str:
    context_parts = []

    for item in retrieved_results:
        metadata = item.get("metadata", {})
        text = metadata.get("text", "")
        source = metadata.get("source", "Unknown")
        page = metadata.get("page", "Unknown")

        cleaned = truncate_text(text, 700)

        if cleaned:
            context_parts.append(f"[Source: {source}, Page: {page}]\n{cleaned}")

    context = "\n\n".join(context_parts)
    q = query.lower()

    if "summarize" in q or "summary" in q:
        instruction = "Write a short summary in 2-3 sentences using your own words."
    elif "main topics" in q or "topics" in q:
        instruction = "List the main topics briefly as bullet points."
    else:
        instruction = "Answer clearly in 1-2 sentences using only the provided context."

    prompt = f"""
You are a helpful document question-answering assistant.

Use only the provided context.
Do not invent information.
If the answer is not clear from the context, say:
"I could not find a clear answer in the retrieved document context."

Instruction:
{instruction}

Context:
{context}

Question:
{query}

Answer:
""".strip()

    return prompt


def fallback_answer(retrieved_results: List[Dict[str, Any]]) -> str:
    texts = []

    for item in retrieved_results[:2]:
        text = item.get("metadata", {}).get("text", "").strip()
        if text:
            texts.append(text)

    if not texts:
        return "I could not find a clear answer in the retrieved document context."

    combined = " ".join(texts)
    return truncate_text(combined, 500)


def format_sources(retrieved_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    sources = []
    seen = set()

    for item in retrieved_results:
        metadata = item.get("metadata", {})

        source = metadata.get("source", "Unknown")
        page = metadata.get("page", "Unknown")
        text = metadata.get("text", "")

        key = (source, page)
        if key in seen:
            continue

        seen.add(key)

        sources.append({
            "source": source,
            "page": page,
            "preview": truncate_text(text, 200)
        })

    return sources


def generate_answer(query: str, retrieved_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not retrieved_results:
        return {
            "answer": "I could not find a clear answer in the retrieved document context.",
            "sources": [],
            "debug_mode": "new_code_loaded"
        }

    sources = format_sources(retrieved_results)
    prompt = build_prompt(query, retrieved_results)

    client = get_client()
    print("Client created:", client is not None)

    if client is None:
        return {
            "answer": fallback_answer(retrieved_results),
            "sources": sources,
            "debug_mode": "new_code_loaded",
            "llm_error": "HF client not initialized"
        }

    try:
        print("Calling HF model...")

        completion = client.chat.completions.create(
            model="moonshotai/Kimi-K2-Instruct-0905",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=200
        )

        print("HF response received")

        answer = completion.choices[0].message.content.strip()
        answer = answer.replace("\n", " ").strip()

        if not answer:
            answer = fallback_answer(retrieved_results)

        return {
            "query": query,   
            "answer": answer,
            "sources": sources
}

    except Exception as e:
        print("HF LLM ERROR:", repr(e))
        return {
            "query": query,
            "answer": fallback_answer(retrieved_results),
            "sources": sources,
            "llm_error": str(e)
        }