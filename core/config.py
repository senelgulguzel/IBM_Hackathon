import os
from dataclasses import dataclass


@dataclass
class Settings:
    api_title: str = os.getenv("API_TITLE", "Customer Complaint Router")
    api_version: str = os.getenv("API_VERSION", "0.1.0")
    qdrant_host: str = os.getenv("QDRANT_HOST", "qdrant")
    qdrant_port: int = int(os.getenv("QDRANT_PORT", "6333"))
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "complaints")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    top_k: int = int(os.getenv("TOP_K", "3"))


settings = Settings()
