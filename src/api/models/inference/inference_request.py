from dataclasses import dataclass
from datetime import datetime

@dataclass
class InferenceRequest:
    model_name: str
    confidence: float
    inference_time_ms: int
    started_at: datetime
    finished_at: datetime
    animal_id: int
    animal_name: str