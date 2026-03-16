from agents.base_agent import BaseAgent


class RoutingAgent(BaseAgent):

    def __init__(self):
        super().__init__("RoutingAgent")

        self.segments = {
            "fraud": "Fraud Investigation Department",
            "loan": "Loan Operations",
            "card": "Card Services",
            "technical": "Digital Banking Support",
            "investment": "Investment Advisory",
            "complaint": "General Complaint Unit"
        }

#ıf it is not possible to determine the intent, route to general complaint unit
    def run(self, context):
        intent = context["intent"]
        return {
            "route_to": self.segments.get(intent, "General Complaint Unit")
        }

#production level routing level would be more complex and may involve multiple factors such as customer value, issue severity, and agent availability.
"""def run(self, context):

    intent = context.get("intent")
    confidence = context.get("confidence", 0)
    similarity_score = context.get("similarity_score", 0)

    # 1️⃣ Intent yok
    if not intent:
        return {
            "route_to": "Manual Review Queue",
            "reason": "Intent missing"
        }

    # 2️⃣ Intent bilinmiyor
    if intent not in self.segments:
        return {
            "route_to": "Manual Review Queue",
            "reason": f"Unknown intent: {intent}"
        }

    # 3️⃣ Confidence düşük
    if confidence < 0.6:
        return {
            "route_to": "Manual Review Queue",
            "reason": "Low confidence score",
            "confidence": confidence
        }

    # 4️⃣ Similarity düşük
    if similarity_score < 0.4:
        return {
            "route_to": "Manual Review Queue",
            "reason": "Low similarity support",
            "similarity_score": similarity_score
        }

    # 5️⃣ Her şey normalse
    return {
        "route_to": self.segments[intent],
        "confidence": confidence,
        "similarity_score": similarity_score
    }
"""