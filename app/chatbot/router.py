# SECTION 1: Imports
from app.prediction.baseline_model import BaselinePredictionEngine


# SECTION 2: Chatbot Router
class AISPChatbotRouter:
    def __init__(self) -> None:
        self.prediction_engine = BaselinePredictionEngine()

    def answer(self, message: str) -> dict:
        lowered = message.lower()
        if "predict" in lowered or "probability" in lowered:
            result = self.prediction_engine.predict_player_hit_probability(0.275, 0.820)
            return {
                "intent": "prediction",
                "answer": f"Baseline prediction: {result.label} = {result.probability}",
                "explanation": result.explanation,
            }
        if "juan soto" in lowered:
            return {
                "intent": "player_lookup",
                "answer": "Search the local database for Juan Soto after running the roster build script.",
            }
        return {
            "intent": "general",
            "answer": "Ask me about MLB teams, rosters, players, stats, or prediction questions.",
        }
