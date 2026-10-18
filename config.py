from dotenv import load_dotenv
import os

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Supported LLM Models on Groq
AVAILABLE_MODELS = [
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-20b",
]

# Models
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")

# Directories
DATA_DIR = os.getenv("DATA_DIR", "./data")
CHROMA_DB = os.getenv("CHROMA_DB", "./vectorstore/chroma_db")

# Chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))

# CRAG Parameters
TOP_K = int(os.getenv("TOP_K", "5"))
MAX_REWRITES = int(os.getenv("MAX_REWRITES", "2"))
MIN_RELEVANT_DOCS = int(os.getenv("MIN_RELEVANT_DOCS", "2"))
RELEVANCE_THRESHOLD = int(os.getenv("RELEVANCE_THRESHOLD", "7"))
MAX_GENERATION_ATTEMPTS = int(os.getenv("MAX_GENERATION_ATTEMPTS", "2"))
ENABLE_WEB_SEARCH = os.getenv("ENABLE_WEB_SEARCH", "true").lower() in ("true", "1", "yes")