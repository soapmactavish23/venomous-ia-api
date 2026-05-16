from dataclasses import dataclass, field
from typing import List

from src.api.models.inference.inference_request import InferenceRequest

@dataclass
class IdentificationResponse:
    scientific_name: str
    ia_description: str
    confidence: float
    inferences: List[InferenceRequest] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "scientificName": self.scientific_name,
            "iaDescription": self.ia_description,
            "confidence": max([item.confidence for item in self.inferences], default=0.0),
            "inferences": [
                {
                    "modelName": item.model_name,
                    "confidence": item.confidence,
                    "inferenceTimeMs": item.inference_time_ms,
                    "startedAt": item.started_at.isoformat(),
                    "finishedAt": item.finished_at.isoformat(),
                    "animalId": item.animal_id,
                }
                for item in self.inferences
            ]
        }