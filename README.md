# IBM_Hackathon

## IBM Hackathon Customer Complaints Project
## Technology Stack

| Layer | Technology | Purpose |
|--------|-------------|-----------|
| 🐍 Backend | Python | Core orchestration logic, agents, routing, pipeline control |
| 🔀 Agent Orchestration | LangFlow 🧩 | Visual + programmatic agent flow design |
| 🗄 Vector Database | Astra DB 🌌 | High-performance vector similarity search |
| 🤖 Large Language Model | IBM Watsonx.ai – Granite 3 8B 🧠⚡ | Reasoning, generation, fallback intelligence |
| 🧬 Architecture | Hybrid RAG + Agentic Routing 🧭 | Decision-centric AI orchestration |
| 🔌 API Layer | FastAPI ⚡ | Real-time inference & orchestration endpoint |
| ☁ Cloud Platform | IBM Cloud ☁️ | Scalable enterprise-grade deployment |


###  The Problem Definition


- Enterprise customer support centers face a structural inefficiency:

- ~70% of customer complaints are repetitive

- Each query is still processed via expensive LLM calls

- This results in:

- High operational cost

- Agent burnout

- Long response latency

- Inconsistent brand messaging

- Traditional RAG systems retrieve documents but still always trigger generation, even when verified solutions already exist.

The core inefficiency:
- AI systems generate when they should remember.

### The Solution

- Solution Overview — Hybrid RAG + Agentic Orchestration

- We propose a Two-Tier Decision Architecture combining:

- Vector Memory (Astra DB)

- Reasoning LLM (IBM Watsonx.ai — ibm/granite-3-8b-instruct)

- Agentic Similarity Router (Meta-Controller)

- Instead of always generating responses, our system decides whether generation is necessary.

- This transforms the architecture from:

- Execution-driven AI → Decision-driven AI

### How It Works

- When a customer submits a complaint, our system:

- Customer Input → Embedding Agent (vectorize)
                        ↓
                 Astra DB Search
                        ↓
                 Parser Agent (structure)
                        ↓
              Similarity Router Agent (decide)
                        ↓
                   IF ≥80% → Return cached response
                   IF <80% → IBM Watsonx Agent (generate)
                        ↓
                  Customer Response

- Converts the query to embeddings and searches Astra DB's vector store
- The Similarity Router analyzes the match confidence using a dynamic threshold (default 80%)
- High confidence (≥80%): Returns the verified cached response instantly—no LLM call needed
- Low confidence (<80%): Routes to IBM Watsonx.ai agent for real-time reasoning and response generation

- This "Two-Tier Decision Architecture" is our key innovation. Unlike traditional RAG systems that always generate responses, our agentic router decides whether generation is necessary, acting as an intelligent traffic controller.

## Operational Flow

- Customer submits a complaint.

- Complaint is converted into vector embeddings.

- Astra DB retrieves top-N semantically similar historical solutions.

- Parser agent normalizes and structures retrieved content.

- Similarity Router Agent evaluates confidence score.

- Routing Logic:

≥ 80% similarity
→ Directly return cached verified solution (no LLM call)

< 80% similarity
→ Forward to IBM Watsonx.ai for real-time reasoning & generation

## Why Judges Haven't Seen This Before

- Most AI systems optimize how well models generate.
- We optimize whether generation is needed at all.

- This introduces:

- Confidence-based routing

- Meta-agent orchestration

- Decision-first AI pipelines

- This system is not a chatbot.

- It is an intelligent complaint orchestration engine.


