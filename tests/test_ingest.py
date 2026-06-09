import re

import pytest

from rag_engine.ingest import chunk_document, load_documents

MAX_WORDS = 150
MIN_WORDS = 8

_docs = load_documents()


# ── helpers ───────────────────────────────────────────────────────────────────


def make_doc(text, *, title="Test Doc", source="test", url="http://example.com"):
    return {"text": text, "title": title, "source": source, "url": url}


# ── fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture(scope="module", params=_docs, ids=[d["title"][:50] for d in _docs])
def doc(request):
    return request.param


@pytest.fixture(scope="module")
def chunked(doc):
    return doc, chunk_document(doc)


# ── load_documents ────────────────────────────────────────────────────────────


def test_load_returns_list():
    assert isinstance(_docs, list)


def test_load_document_count():
    assert len(_docs) == 10, f"Expected 10 docs, got {len(_docs)}"


def test_doc_has_required_keys(doc):
    assert {"text", "title", "source", "url"} <= doc.keys()


def test_doc_text_nonempty(doc):
    assert len(doc["text"].strip()) > 0


def test_doc_no_frontmatter_bleed(doc):
    assert not doc["text"].startswith("---"), "Frontmatter leaked into text body"


def test_doc_url_is_http(doc):
    assert doc["url"].startswith("http"), f"Unexpected URL: {doc['url']!r}"


# ── chunk_document: output contract ──────────────────────────────────────────


def test_chunk_returns_required_keys(chunked):
    _, result = chunked
    assert {"chunks", "metadatas", "ids"} <= result.keys()


def test_chunk_lists_same_length(chunked):
    _, result = chunked
    assert len(result["chunks"]) == len(result["metadatas"]) == len(result["ids"])


def test_chunk_at_least_one_chunk(chunked):
    _, result = chunked
    assert len(result["chunks"]) > 0


def test_chunk_word_bounds(chunked):
    _, result = chunked
    for i, chunk in enumerate(result["chunks"]):
        wc = len(chunk.split())
        assert wc >= MIN_WORDS, f"Chunk {i}: too short ({wc} words)"
        assert wc <= MAX_WORDS, f"Chunk {i}: too long ({wc} words)"


def test_chunk_ids_unique(chunked):
    _, result = chunked
    ids = result["ids"]
    assert len(ids) == len(set(ids)), f"{len(ids) - len(set(ids))} duplicate IDs"


def test_chunk_metadata_matches_doc(chunked):
    doc, result = chunked
    for i, meta in enumerate(result["metadatas"]):
        assert {"title", "source", "url"} <= meta.keys(), f"Chunk {i} missing keys"
        assert meta["title"] == doc["title"], f"Chunk {i} title mismatch"
        assert meta["url"] == doc["url"], f"Chunk {i} URL mismatch"


# ── chunk_document: header-aware strategy (unit tests) ───────────────────────


def test_header_section_kept_as_single_chunk():
    """A short header+body that fits within max_words is not split."""
    text = "## Dining Options\n\nThe university has several dining halls and cafes on campus."
    result = chunk_document(make_doc(text))
    assert len(result["chunks"]) == 1
    assert result["chunks"][0].startswith("## Dining Options")


def test_small_sections_grouped_together():
    """Two sections each well under target_words are merged into one chunk."""
    body = "word " * 40  # 40 words
    text = f"## Section A\n\n{body}\n\n## Section B\n\n{body}"
    result = chunk_document(make_doc(text))
    assert len(result["chunks"]) == 1, (
        f"Expected 1 chunk for two small sections, got {len(result['chunks'])}"
    )


def test_oversized_section_falls_back_to_paragraphs():
    """A section exceeding max_words with two paragraphs produces multiple chunks."""
    para = "word " * 90  # 90 words per paragraph
    text = f"## Big Section\n\n{para}\n\n{para}"
    result = chunk_document(make_doc(text))
    assert len(result["chunks"]) >= 2


def test_oversized_paragraph_falls_back_to_sentences():
    """A single oversized paragraph is split at sentence boundaries, never exceeding max_words."""
    sentence = "This is a complete sentence with eight words. "
    big_para = sentence * 25  # ~200 words in one paragraph block
    text = f"## Section\n\n{big_para}"
    result = chunk_document(make_doc(text))
    assert len(result["chunks"]) >= 2
    for i, chunk in enumerate(result["chunks"]):
        wc = len(chunk.split())
        assert wc <= MAX_WORDS, f"Chunk {i}: {wc} words exceeds MAX_WORDS ({MAX_WORDS})"


def test_no_overlap_between_consecutive_chunks():
    """Chunks are flushed clean — no sliding-window word overlap between neighbours."""
    sentence = "This is a complete sentence about something interesting. "
    text = "## Topic\n\n" + sentence * 30
    result = chunk_document(make_doc(text))
    chunks = result["chunks"]
    if len(chunks) < 2:
        pytest.skip("Not enough chunks to test overlap")
    for i in range(len(chunks) - 1):
        tail = chunks[i].split()[-10:]
        head = chunks[i + 1].split()[:10]
        assert tail != head, (
            f"Unexpected overlap between chunk {i} and {i + 1}:\n"
            f"  tail={tail}\n  head={head}"
        )


def test_no_chunk_cuts_mid_sentence():
    """Every chunk either ends with sentence-ending punctuation or is a header/list line."""
    sentence = "This is a complete sentence with eight words. "
    big_para = sentence * 25
    text = f"## Section\n\n{big_para}"
    result = chunk_document(make_doc(text))
    for i, chunk in enumerate(result["chunks"]):
        last_line = chunk.rstrip().splitlines()[-1]
        assert re.search(r"[.!?]$", last_line) or last_line.startswith("#"), (
            f"Chunk {i} last line appears to be cut mid-sentence: {last_line!r}"
        )


# ── verbose output ────────────────────────────────────────────────────────────


def test_show_chunks(chunked, show_chunks):
    """Verbose output — run with: pytest --show-chunks -s"""
    if not show_chunks:
        pytest.skip("Pass --show-chunks to enable")
    doc, result = chunked
    print(f"\n{'=' * 60}")
    print(f"Document : {doc['title']}")
    print(f"Source   : {doc['source']}")
    print(f"URL      : {doc['url']}")
    print(f"Chunks   : {len(result['chunks'])}")
    for i, chunk in enumerate(result["chunks"]):
        print(f"\n  -- chunk {i}  ({len(chunk.split())} words) --")
        print(f"  {chunk}")
