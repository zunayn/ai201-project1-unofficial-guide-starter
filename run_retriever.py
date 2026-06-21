# run_retrieval.py
from ingest import load_documents, chunk_document
from retriever import embed_and_store, retrieve, get_collection

def setup_db():
    collection = get_collection()
    # Check if the DB is already populated so we don't duplicate
    if collection.count() == 0:
        print("Populating vector database...")
        docs = load_documents()
        all_chunks = []
        for doc in docs:
            all_chunks.extend(chunk_document(doc["text"], doc["game"]))
        embed_and_store(all_chunks)
    else:
        print(f"Database already populated with {collection.count()} chunks.")

def test_queries():
    queries = [
        "Who should I take for Data Structures (CS 3358)?",
        "Is Dr. Mylene Farias a good choice for Computer Architecture (CS 3339)?",
        "Where are the best places to study near Derrick Hall?"
    ]
    
    for i, q in enumerate(queries, 1):
        print(f"\n{'='*50}\nQuery {i}: {q}\n{'='*50}")
        results = retrieve(q, n_results=3)
        
        for idx, res in enumerate(results, 1):
            print(f"\n[Result {idx}] Source: {res['game']} | Distance: {res['distance']:.4f}")
            print(f"Text: {res['text']}")

if __name__ == "__main__":
    setup_db()
    test_queries()