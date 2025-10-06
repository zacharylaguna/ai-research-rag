"""Configuration settings for the RAG system."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings."""
    
    # API settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # ChromaDB settings
    CHROMA_PERSIST_DIRECTORY: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    CHROMA_COLLECTION_NAME: str = "documents"
    
    # Model settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama2")
    
    # Document processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Retrieval settings
    SIMILARITY_TOP_K: int = 5
    
    # Optional OpenAI settings (for Agno if using OpenAI models)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Agno settings
    AGNO_API_KEY: str = os.getenv("AGNO_API_KEY", "")  # For Agno monitoring (optional)
    
    # Ollama settings
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Global settings instance
settings = Settings()
