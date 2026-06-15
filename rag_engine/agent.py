from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_CLIENT: Groq | None = None
_MODEL = "llama-3.3-70b-versatile"

_SYSTEM_PROMPT = """\
You are a friendly and helpful local guide for George Mason University (GMU) students and the DMV area \
(DC, Maryland, Virginia).
Your knowledge comes exclusively from the retrieved sources provided below.

Rules:
1. Only recommend locations, events, or activities that appear in the retrieved sources.
2. For every recommendation, cite the source title and URL in your answer.
3. If the retrieved sources do not contain information that answers the question, say so clearly \
   and do not make up an answer.
4. If the question is outside your domain (GMU student life, local events, DMV-area dining and \
   activities), politely decline and explain your scope is limited to GMU and the DMV area.
5. Do not invent, hallucinate, or extrapolate beyond what the sources say.
6. Use the conversation history (prior messages) to understand follow-up questions, resolve \
   pronouns, and maintain continuity — but ground every answer in the current retrieved sources.\
"""


def _get_client() -> Groq:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    return _CLIENT


def _build_context(chunks: list[dict]) -> str:
    parts = []
    for i, chunk in enumerate(chunks, 1):
        meta = chunk["metadata"]
        title = meta.get("title", "Unknown")
        source = meta.get("source", "")
        url = meta.get("url", "N/A")
        parts.append(
            f"[Source {i}] {title} ({source})\n"
            f"URL: {url}\n"
            f"{chunk['text']}"
        )
    return "\n\n---\n\n".join(parts)


def generate_response(
    query: str,
    retrieved_chunks: list[dict],
    history: list[dict] | None = None,
) -> dict:
    """Generate a grounded response from retrieved chunks using Groq.

    Args:
        query: The user's current question.
        retrieved_chunks: Output from retrieve() for the current query.
        history: Prior turns as a list of {"role": "user"|"assistant", "content": str}
                 dicts. Pass [] or omit for a fresh conversation.

    Returns:
        dict with:
          - "answer": str — the LLM response
          - "sources": list[str] — deduplicated attribution lines for display
    """
    if not retrieved_chunks:
        return {
            "answer": (
                "I couldn't find any relevant information for your query in my sources. "
                "I cover GMU student life and activities in the DMV area — try rephrasing "
                "or asking about local events, dining, or things to do near campus."
            ),
            "sources": [],
        }

    context = _build_context(retrieved_chunks)
    user_message = f"Context:\n{context}\n\nQuestion: {query}"

    messages: list[Any] = [{"role": "system", "content": _SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = _get_client().chat.completions.create(
        model=_MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=1024,
    )

    answer = response.choices[0].message.content

    # Deduplicate sources by URL for the display list
    seen: set[str] = set()
    sources: list[str] = []
    for chunk in retrieved_chunks:
        meta = chunk["metadata"]
        url = meta.get("url", "")
        if url not in seen:
            seen.add(url)
            label = meta.get("title") or meta.get("source") or "Unknown source"
            sources.append(f"{label} — {url}" if url else label)

    return {"answer": answer, "sources": sources}
