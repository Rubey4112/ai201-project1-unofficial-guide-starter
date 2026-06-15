from __future__ import annotations

from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

_DB_PATH = Path(__file__).parent.parent / "chroma_db"
_COLLECTION_NAME = "gmu_guide"
_EMBED_MODEL = "all-MiniLM-L6-v2"
_populated = False


def _get_collection() -> chromadb.Collection:
    ef = SentenceTransformerEmbeddingFunction(model_name=_EMBED_MODEL)
    client = chromadb.PersistentClient(path=str(_DB_PATH))
    return client.get_or_create_collection(name=_COLLECTION_NAME, embedding_function=ef)


def _populate_db() -> None:
    global _populated
    if _populated or _DB_PATH.exists():
        _populated = True
        return
    from rag_engine.ingest import chunk_document, load_documents
    print("ChromaDB not found — ingesting documents...")
    docs = load_documents()
    chunk_results = [chunk_document(doc) for doc in docs]
    total = sum(len(r["chunks"]) for r in chunk_results)
    embed_and_store(chunk_results)
    _populated = True
    print(f"Stored {total} chunks from {len(docs)} documents.")


def embed_and_store(chunk_results: list[dict]) -> None:
    """Flatten chunk_document() outputs and upsert into ChromaDB."""
    collection = _get_collection()

    all_texts: list[str] = []
    all_metadatas: list[dict] = []
    all_ids: list[str] = []

    for result in chunk_results:
        all_texts.extend(result["chunks"])
        all_metadatas.extend(result["metadatas"])
        all_ids.extend(result["ids"])

    if not all_texts:
        return

    collection.upsert(documents=all_texts, metadatas=all_metadatas, ids=all_ids)


def retrieve(query: str, top_k: int = 7) -> list[dict]:
    """Return top_k chunks for query, each with text, metadata, and distance."""
    _populate_db()
    collection = _get_collection()
    results = collection.query(query_texts=[query], n_results=top_k)

    return [
        {"text": text, "metadata": meta, "distance": dist}
        for text, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]
