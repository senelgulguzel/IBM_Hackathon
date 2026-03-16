from agents.base_agent import BaseAgent


class IntentAgent(BaseAgent):
    def __init__(self, qdrant):
        super().__init__("IntentAgent")
        self.qdrant = qdrant

    def run(self, context):
        vector = context["vector"]
        text = context["text"].lower()
        similar_cases = self.qdrant.search(vector)

        if "kredi" in text:
            intent = "loan"
        elif "kart" in text:
            intent = "card"
        elif "dolandir" in text:
            intent = "fraud"
        elif "uygulama" in text:
            intent = "technical"
        else:
            intent = "complaint"

        confidence = 0.75 if similar_cases else 0.45
        return {
            "intent": intent,
            "confidence": confidence,
            "similar_cases": similar_cases,
        }
