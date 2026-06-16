# SECTION 1: Imports
from dataclasses import dataclass


# SECTION 2: Prediction Result
@dataclass
class PredictionResult:
    label: str
    probability: float
    explanation: str


# SECTION 3: Baseline Prediction Engine
class BaselinePredictionEngine:
    def predict_player_hit_probability(self, batting_average: float | None, ops: float | None) -> PredictionResult:
        avg = batting_average or 0.240
        ops_value = ops or 0.700
        probability = min(max((avg * 0.65) + (ops_value * 0.20), 0.05), 0.75)
        return PredictionResult(
            label="hit_probability",
            probability=round(probability, 4),
            explanation="Baseline estimate using batting average and OPS. Replace with trained models later.",
        )
