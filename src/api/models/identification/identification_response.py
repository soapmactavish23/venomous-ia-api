from dataclasses import dataclass, field
from typing import List

from src.api.models.inference.inference_request import InferenceRequest

@dataclass
class IdentificationResponse:
    scientific_name: str
    ia_description: str
    confidence: float
    inferences: List[InferenceRequest] = field(default_factory=list)