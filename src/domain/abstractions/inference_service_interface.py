from abc import ABC, abstractmethod
from typing import List

from src.api.models.inference.inference_request import InferenceRequest

class InferenceServiceInterface(ABC):
    @abstractmethod
    def predict_all(self, image_file) -> List[InferenceRequest]: pass