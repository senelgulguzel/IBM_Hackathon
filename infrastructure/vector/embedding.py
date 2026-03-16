from hashlib import sha256
from typing import List

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        try:
            self.model = SentenceTransformer(model_name)
        except Exception:
            # Keep API available even if model download is unavailable.
            self.model = None

    def embed(self, text: str) -> List[float]:
        if self.model is not None:
            return self.model.encode(text).tolist()
        return self._fallback_embedding(text)

    def _fallback_embedding(self, text: str) -> List[float]:
        digest = sha256(text.encode("utf-8")).digest()
        return [byte / 255.0 for byte in digest]
