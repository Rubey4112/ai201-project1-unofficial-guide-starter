"""Interactive CLI for testing the retrieve() function."""

import sys

from rag_engine.retriever import retrieve

TOP_K = 7


def main() -> None:
    print("RAG Retrieval Tester — type a query and press Enter (Ctrl+C to quit)\n")

    while True:
        try:
            query = input("Query: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            sys.exit(0)

        if not query:
            continue

        chunks = retrieve(query, top_k=TOP_K)

        if not chunks:
            print("  (no results)\n")
            continue

        print(f"\n  Top {len(chunks)} chunks for: \"{query}\"\n")
        for i, chunk in enumerate(chunks, 1):
            meta = chunk["metadata"]
            print(f"  [{i}] distance: {chunk['distance']:.4f}")
            print(f"      source:   {meta.get('source', '?')} — {meta.get('title', '?')}")
            print(f"      url:      {meta.get('url', '?')}")
            print(f"      text:     {chunk['text'][:300]}{'...' if len(chunk['text']) > 300 else ''}")
            print()


if __name__ == "__main__":
    main()
