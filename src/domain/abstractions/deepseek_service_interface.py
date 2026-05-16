from abc import ABC, abstractmethod
from typing import Optional, List

from src.api.models.inference.inference_request import InferenceRequest


class DeepSeekServiceInterface(ABC):
    @abstractmethod
    def analyze(self, description: Optional[str], animal_name: Optional[str],
                audio_transcription: Optional[str], inferences: List[InferenceRequest],) -> dict: pass
