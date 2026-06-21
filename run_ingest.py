# run_ingest.py
from ingest import load_documents, chunk_document
import random

def test_pipeline():
    print("--- Verifying Milestone 3: Ingestion Pipeline ---\n")
    documents = load_documents()
    
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc["text"], doc["game"])
        all_chunks.extend(chunks)
        
    print(f"\nTotal chunks generated across all files: {len(all_chunks)}\n")
    
    print("--- 5 Random Sample Chunks ---")
    sample_chunks = random.sample(all_chunks, min(5, len(all_chunks)))
    for i, chunk in enumerate(sample_chunks, 1):
        print(f"\n[Chunk {i}] Source: {chunk['game']}")
        print(f"Text: {chunk['text']}")
        print("-" * 40)

if __name__ == "__main__":
    test_pipeline()