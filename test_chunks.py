import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rag_engine.ingest import load_documents, chunk_document

docs = load_documents()

for doc in docs:
    result = chunk_document(doc)
    print(f"\n{'='*60}")
    print(f"DOC: {doc['title']}")
    print(f"Total chunks: {len(result['chunks'])}")
    print(f"{'='*60}")
    for i, chunk in enumerate(result["chunks"]):
        print(f"\n--- Chunk {i+1} ({len(chunk.split())} words) ---")
        print(chunk)
