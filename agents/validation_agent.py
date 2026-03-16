from agents.base_agent import BaseAgent


class ValidationAgent(BaseAgent):

    def __init__(
        self,
        required_fields=None,
        min_confidence=0.6,
        min_similarity=0.4
    ):
        super().__init__(name="ValidationAgent")

        self.required_fields = required_fields or ["intent"]
        self.min_confidence = min_confidence
        self.min_similarity = min_similarity

    def run(self, context: dict) -> dict:

        # 1️⃣ Required fields kontrolü
        for field in self.required_fields:
            if field not in context:
                return {
                    "valid": False,
                    "reason": f"Missing required field: {field}"
                }

        intent = context.get("intent")
        confidence = context.get("confidence", 0)
        similarity_score = context.get("similarity_score", 0)

        # 2️⃣ Intent boş mu?
        if not intent:
            return {
                "valid": False,
                "reason": "Intent is empty"
            }

        # 3️⃣ Confidence düşük mü?
        if confidence < self.min_confidence:
            return {
                "valid": False,
                "reason": "Low confidence",
                "confidence": confidence
            }

        # 4️⃣ Similarity düşük mü?
        if similarity_score < self.min_similarity:
            return {
                "valid": False,
                "reason": "Low similarity support",
                "similarity_score": similarity_score
            }

        # 5️⃣ Her şey OK
        return {
            "valid": True
        }