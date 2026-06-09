import pytest

from rag_engine.ingest import chunk_document, load_documents

CHUNK_SIZE = 150
OVERLAP = 8
MIN_WORDS = 8

# Load once at collection time so both fixture sets share the same data.
_docs = load_documents()


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


# ── chunk_document ────────────────────────────────────────────────────────────


def test_chunk_returns_required_keys(chunked):
    _, result = chunked
    assert {"chunks", "metadatas", "ids"} <= result.keys()


def test_chunk_lists_same_length(chunked):
    _, result = chunked
    assert len(result["chunks"]) == len(result["metadatas"]) == len(result["ids"])


def test_chunk_at_least_one_chunk(chunked):
    _, result = chunked
    assert len(result["chunks"]) > 0


def test_chunk_word_counts(chunked):
    _, result = chunked
    for i, chunk in enumerate(result["chunks"]):
        word_count = len(chunk.split())
        assert word_count >= MIN_WORDS, f"Chunk {i}: too short ({word_count} words)"
        assert word_count <= CHUNK_SIZE, f"Chunk {i}: too long ({word_count} words)"


def test_chunk_ids_unique(chunked):
    _, result = chunked
    ids = result["ids"]
    duplicates = len(ids) - len(set(ids))
    assert duplicates == 0, f"{duplicates} duplicate IDs found"


def test_chunk_metadata_matches_doc(chunked):
    doc, result = chunked
    for i, meta in enumerate(result["metadatas"]):
        assert {"title", "source", "url"} <= meta.keys(), f"Chunk {i} missing metadata keys"
        assert meta["title"] == doc["title"], f"Chunk {i} title mismatch"
        assert meta["url"] == doc["url"], f"Chunk {i} URL mismatch"


def test_chunk_overlap(chunked):
    _, result = chunked
    chunks = result["chunks"]
    if len(chunks) < 2:
        pytest.skip("Not enough chunks to check overlap")
    tail = chunks[0].split()[-OVERLAP:]
    head = chunks[1].split()[:OVERLAP]
    assert tail == head, f"Expected {OVERLAP}-word overlap:\n  tail={tail}\n  head={head}"


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
