from abc import ABC, abstractmethod
import time
import traceback


class BaseAgent(ABC):

    def __init__(self, name: str):
        self.name = name

    def execute(self, context: dict) -> dict:
        """
        Wrapper method.
        All agents should be executed via this method.
        """

        start_time = time.time()

        try:
            self._validate_context(context)

            result = self.run(context)

            return {
                "agent": self.name,
                "status": "success",
                "execution_time": round(time.time() - start_time, 4),
                "result": result
            }

        except Exception as e:
            return {
                "agent": self.name,
                "status": "error",
                "execution_time": round(time.time() - start_time, 4),
                "error": str(e),
                "trace": traceback.format_exc()
            }

    @abstractmethod
    def run(self, context: dict) -> dict:
        """
        Core logic of the agent.
        Must be implemented in child classes.
        """
        pass

    def _validate_context(self, context: dict):
        if not isinstance(context, dict):
            raise ValueError("Context must be a dictionary.")