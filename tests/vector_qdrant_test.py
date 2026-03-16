from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams,Distance,PointStruct
from sentence_transformers import SentenceTransformer
import uuid

client= QdrantClient("localhost", port=6333)

collection_name= "ai_docs"

model= SentenceTransformer('all-MiniLM-L6-v2')

client.recreate_collection(
    collection_name= collection_name,
    vectors_config= VectorParams(size=384, distance= Distance.COSINE)
)

texts= [
    "This is the first document.",
    "This is the second document.",
    "This is the third document."]

vectors= model.encode(texts)

points= [
    PointStruct(
        id= str(uuid.uuid4()),
        vector= vectors[i].tolist(),
        payload={"text": texts[i]}
    )
    for i in range(len(texts))
]
client.upsert(
    collection_name= collection_name,
    points= points
)
print("Documents inserted into Qdrant collection.")