class OrchestratorAgent:
    def __init__(self, intent_agent, validation_agent, routing_agent):
        self.intent_agent = intent_agent
        self.validation_agent = validation_agent
        self.routing_agent = routing_agent

    def run(self, context: dict) -> dict:
        intent_result = self.intent_agent.run(context)

        similar_cases = intent_result.get("similar_cases") or []
        top_similarity = 0.0
        if similar_cases:
            top_similarity = float(similar_cases[0].get("score", 0.0) or 0.0)

        validation_input = {
            "intent": intent_result.get("intent"),
            "confidence": float(intent_result.get("confidence", 0.0)),
            "similarity_score": top_similarity,
        }
        validation_result = self.validation_agent.run(validation_input)

        if not validation_result.get("valid"):
            return {
                "status": "needs_manual_review",
                "intent": intent_result.get("intent"),
                "validation": validation_result,
                "route": "Manual Review Queue",
                "similar_cases": similar_cases,
            }

        routing_result = self.routing_agent.run(intent_result)
        return {
            "status": "ok",
            "intent": intent_result.get("intent"),
            "confidence": float(intent_result.get("confidence", 0.0)),
            "validation": validation_result,
            "route": routing_result["route_to"],
            "similar_cases": similar_cases,
        }
