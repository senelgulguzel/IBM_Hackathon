class CustomerComplaintPipeline:
    def __init__(self, orchestrator, embedding_service):
        self.orchestrator = orchestrator
        self.embedding_service = embedding_service

    def process(self, customer_text: str):
        vector = self.embedding_service.embed(customer_text)
        context = {"text": customer_text, "vector": vector}
        return self.orchestrator.run(context)
