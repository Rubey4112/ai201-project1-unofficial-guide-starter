import hashlib
import re
from pathlib import Path

DOCUMENTS_DIR = Path(__file__).parent.parent / "documents"


def _parse_frontmatter(content: str) -> tuple[dict, str]:
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return {}, content
    body = content[match.end():]
    metadata = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            metadata[key.strip()] = value.strip().strip('"')
    return metadata, body


def load_documents() -> list[dict]:
    """
    Load all .md files from the documents folder.

    Returns a list of dicts, each with:
        text   — body text (frontmatter stripped)
        title  — document title
        source — source name (e.g. "r/gmu")
        url    — link to original document
    """
    docs = []
    for path in sorted(DOCUMENTS_DIR.glob("*.md")):
        if path.name == ".gitkeep":
            continue
        content = path.read_text(encoding="utf-8")
        metadata, body = _parse_frontmatter(content)
        docs.append(
            {
                "text": body.strip(),
                "title": metadata.get("title", path.stem),
                "source": metadata.get("source", ""),
                "url": metadata.get("url", ""),
            }
        )
    return docs


def chunk_document(doc: dict) -> dict:
    """
    Chunk a single document by markdown header, then paragraph, then sentence.

    Each `#`-prefixed header starts a new section. Sections within max_words
    are kept whole; oversized sections fall back to paragraph then sentence
    splits. Small segments are grouped until target_words is reached.

    Returns a dict with:
        chunks    — list of chunk strings
        metadatas — list of dicts (title, source, url) — one per chunk
        ids       — list of unique SHA-256 hex strings for ChromaDB deduplication
    """
    target_words = 100
    max_words = 150
    min_words = 8

    # Split on markdown headers (##, ###, etc.), keeping the header line with its section
    header_sections = re.split(r"(?=^#{1,6}\s)", doc["text"], flags=re.MULTILINE)

    segments: list[str] = []
    for section in header_sections:
        section = section.strip()
        if not section:
            continue
        if len(section.split()) <= max_words:
            segments.append(section)
        else:
            for para in re.split(r"\n\s*\n", section):
                para = para.strip()
                if not para:
                    continue
                if len(para.split()) <= max_words:
                    segments.append(para)
                else:
                    for sent in re.split(r"(?<=[.!?])\s+", para):
                        if sent.strip():
                            segments.append(sent.strip())

    chunks: list[str] = []
    current_parts: list[str] = []
    current_wc = 0

    for seg in segments:
        seg_wc = len(seg.split())
        if current_parts and current_wc + seg_wc > max_words:
            if current_wc >= min_words:
                chunks.append("\n\n".join(current_parts))
            current_parts, current_wc = [], 0
        current_parts.append(seg)
        current_wc += seg_wc
        if current_wc >= target_words:
            if current_wc >= min_words:
                chunks.append("\n\n".join(current_parts))
            current_parts, current_wc = [], 0

    if current_parts and current_wc >= min_words:
        chunks.append("\n\n".join(current_parts))

    meta = {"title": doc["title"], "source": doc["source"], "url": doc["url"]}
    metadatas = [meta for _ in chunks]
    ids = [
        hashlib.sha256(f"{doc['url']}::chunk_{i}".encode()).hexdigest()[:32]
        for i in range(len(chunks))
    ]

    return {"chunks": chunks, "metadatas": metadatas, "ids": ids}
