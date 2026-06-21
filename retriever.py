# retriever.py
import chromadb
from chromadb.utils import embedding_functions
import config

# Initialize the local persistent Chroma client and embedding function
_client = chromadb.PersistentClient(path=config.CHROMA_PATH)
_embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=config.EMBEDDING_MODEL
)

def get_collection():
    """Return the ChromaDB collection using cosine similarity."""
    return _client.get_or_create_collection(
        name=config.CHROMA_COLLECTION,
        embedding_function=_embedding_function,
        metadata={"hnsw:space": "cosine"}
    )

def embed_and_store(chunks):
    """
    Embed a list of chunks and store them in the vector database.
    """
    collection = get_collection()
    
    if not chunks:
        print("No chunks provided to store.")
        return

    documents = [c["text"] for c in chunks]
    # Store the source document name as metadata for attribution later
    metadatas = [{"game": c["game"]} for c in chunks]  
    ids = [c["chunk_id"] for c in chunks]

    # ChromaDB will automatically embed the text using all-MiniLM-L6-v2
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Stored {len(chunks)} total chunks in the vector database.")

def retrieve(query, n_results=None):
    """
    Find the most relevant document chunks for a user's question.
    """
    if n_results is None:
        n_results = config.N_RESULTS # Defaults to 5

    collection = get_collection()
    
    # Run semantic search query using ChromaDB
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    # Restructure the nested lists from ChromaDB into a clean list of dicts
    retrieved_chunks = []
    if results and results["documents"] and len(results["documents"][0]) > 0:
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        for i in range(len(docs)):
            retrieved_chunks.append({
                "text": docs[i],
                "game": metas[i].get("game", "Unknown Source"),
                "distance": distances[i] # Lower distance = better match (for cosine)
            })

    return retrieved_chunks