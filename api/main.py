import os
import sys
from contextlib import asynccontextmanager

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agents.intent_agent import IntentAgent
from agents.routing_agent import RoutingAgent
from agents.validation_agent import ValidationAgent
from core.config import settings
from core.orchestrator import OrchestratorAgent
from infrastructure.vector.embedding import EmbeddingService
from infrastructure.vector.qdrant_client import QdrantService
from services.customer_pipeline import CustomerComplaintPipeline


class ComplaintRequest(BaseModel):
    text: str = Field(..., min_length=3, description="Customer complaint text")


class ComplaintResponse(BaseModel):
    status: str
    intent: str | None = None
    route: str
    confidence: float | None = None
    validation: dict
    similar_cases: list


embedding_service = EmbeddingService(model_name=settings.embedding_model)
qdrant_service = QdrantService(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
    collection_name=settings.qdrant_collection,
    top_k=settings.top_k,
)
intent_agent = IntentAgent(qdrant=qdrant_service)
validation_agent = ValidationAgent()
routing_agent = RoutingAgent()
orchestrator = OrchestratorAgent(
    intent_agent=intent_agent,
    validation_agent=validation_agent,
    routing_agent=routing_agent,
)
pipeline = CustomerComplaintPipeline(
    orchestrator=orchestrator,
    embedding_service=embedding_service,
)

SAMPLE_DATASET = [
    {
        "id": 1,
        "customer_id": "C001",
        "text": "Kredi basvurum reddedildi, sebebini ogrenmek istiyorum.",
        "expected_intent": "loan",
    },
    {
        "id": 2,
        "customer_id": "C002",
        "text": "Kredi kartimdan bilgim disinda harcama yapildi.",
        "expected_intent": "card",
    },
    {
        "id": 3,
        "customer_id": "C003",
        "text": "Uygulama surekli hata veriyor ve giris yapamiyorum.",
        "expected_intent": "technical",
    },
    {
        "id": 4,
        "customer_id": "C004",
        "text": "Dolandiricilik supheli bir transfer goruyorum.",
        "expected_intent": "fraud",
    },
    {
        "id": 5,
        "customer_id": "C005",
        "text": "Musteri hizmetlerinden memnun degilim, sikayet kaydi acmak istiyorum.",
        "expected_intent": "complaint",
    },
]

@asynccontextmanager
async def lifespan(_app: FastAPI):
    for row in SAMPLE_DATASET:
        vector = embedding_service.embed(row["text"])
        qdrant_service.upsert_case(row["text"], vector)
    yield


app = FastAPI(title=settings.api_title, version=settings.api_version, lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/complaints/process", response_model=ComplaintResponse)
def process_complaint(payload: ComplaintRequest):
    try:
        result = pipeline.process(payload.text)
        return ComplaintResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/dataset/sample")
def get_sample_dataset():
    return {"count": len(SAMPLE_DATASET), "items": SAMPLE_DATASET}


@app.post("/dataset/run-sample")
def run_sample_dataset():
    results = []
    matched = 0

    for row in SAMPLE_DATASET:
        output = pipeline.process(row["text"])
        predicted_intent = output.get("intent")
        is_match = predicted_intent == row["expected_intent"]
        if is_match:
            matched += 1

        results.append(
            {
                "id": row["id"],
                "customer_id": row["customer_id"],
                "text": row["text"],
                "expected_intent": row["expected_intent"],
                "predicted_intent": predicted_intent,
                "route": output.get("route"),
                "status": output.get("status"),
                "match": is_match,
            }
        )

    accuracy = matched / len(SAMPLE_DATASET) if SAMPLE_DATASET else 0.0
    return {
        "total": len(SAMPLE_DATASET),
        "matched": matched,
        "accuracy": round(accuracy, 4),
        "results": results,
    }
