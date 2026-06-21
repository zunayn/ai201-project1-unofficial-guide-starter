# ingest.py
import os
import config
import re

def clean_text(text):
    """
    Removes unwanted artifacts, normalizes whitespace, and strips leftover HTML.
    """
    # Remove any stray HTML tags just in case
    text = re.sub(r'<[^>]+>', '', text)
    # Normalize multiple spaces and newlines into single spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_documents():
    """Loads all .txt rule documents from the docs folder."""
    documents = []
    if not os.path.exists(config.DOCS_PATH):
        os.makedirs(config.DOCS_PATH)
        
    for filename in os.listdir(config.DOCS_PATH):
        if filename.endswith(".txt"):
            filepath = os.path.join(config.DOCS_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw_text = f.read()
                
            clean_content = clean_text(raw_text)
            
            if len(clean_content) > 0:
                # Use the filename (without extension) as the source label
                source_name = filename.replace('.txt', '')
                documents.append({"text": clean_content, "game": source_name})
                
    print(f"Loaded and cleaned {len(documents)} document(s).")
    return documents

def chunk_document(text, game):
    """
    Split a rule document into chunks ready for embedding using a sliding window.
    """
    chunk_size = 300
    overlap = 50
    min_length = 50
    chunks = []
    
    start = 0
    counter = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip()
        
        if len(chunk_text) >= min_length:
            chunks.append({
                "text": chunk_text,
                "game": game,
                "chunk_id": f"{game}_{counter}"
            })
            counter += 1
            
        start += (chunk_size - overlap)
        
    return chunks