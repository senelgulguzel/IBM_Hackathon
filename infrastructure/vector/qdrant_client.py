from typing import Dict, List
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


class QdrantService:
    def __init__(self, host: str, port: int, collection_name: str, top_k: int = 3):
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.top_k = top_k
        self.client = None
        self._fallback_points: List[Dict] = []

        try:
            self.client = QdrantClient(host=host, port=port)
            self.client.get_collections()
        except Exception:
            self.client = None

    def ensure_collection(self, vector_size: int):
        if self.client is None:
            return

        collections = self.client.get_collections().collections
        exists = any(item.name == self.collection_name for item in collections)
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

    def upsert_case(self, text: str, vector: List[float]):
        payload = {"text": text}
        if self.client is None:
            self._fallback_points.append({"vector": vector, "payload": payload, "score": 0.5})
            return

        self.ensure_collection(len(vector))
        point = PointStruct(id=str(uuid.uuid4()), vector=vector, payload=payload)
        self.client.upsert(collection_name=self.collection_name, points=[point])

    def search(self, vector: List[float]) -> List[Dict]:
        if self.client is None:
            return self._fallback_points[: self.top_k]

        self.ensure_collection(len(vector))
        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=self.top_k,
        )
        return [
            {
                "id": str(hit.id),
                "score": float(hit.score),
                "payload": hit.payload or {},
            }
            for hit in hits
        ]
