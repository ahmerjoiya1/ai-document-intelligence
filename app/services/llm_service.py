def build_prompt(query: str, retrieved_results: list) -> str:
    context_parts = []

    for item in retrieved_results:
        metadata = item["metadata"]
        text = metadata.get("text", "")
        page = metadata.get("page", "")
        source = metadata.get("source", "")

        context_parts.append(f"[Source: {source}, Page: {page}]\n{text}")

    context = "\n\n".join(context_parts)

    prompt = f"""Context:
{context}

Question:
{query}

Answer:
"""
    return prompt


def generate_answer(query: str, retrieved_results: list) -> str:
    if not retrieved_results:
        return "I could not find a clear answer in the retrieved document context."

    top_text = retrieved_results[0]["metadata"].get("text", "")[:2000].strip()

    if not top_text:
        return "I could not find a clear answer in the retrieved document context."

    return top_text.strip()