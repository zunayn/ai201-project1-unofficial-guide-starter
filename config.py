import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# API Keys and Models
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Database Configuration
CHROMA_COLLECTION = "unofficial_guide"  # You can change this collection name if you want
CHROMA_PATH = "./chroma_db"
N_RESULTS = 5

# File Paths
DOCS_PATH = "./documents"