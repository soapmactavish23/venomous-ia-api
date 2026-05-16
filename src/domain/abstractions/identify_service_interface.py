from abc import ABC, abstractmethod

from src.api.models.identification.identification_request import IdentificationRequest
from src.api.models.identification.identification_response import IdentificationResponse

class IdentifyServiceInterface(ABC):
    @abstractmethod
    def identify(self, request: IdentificationRequest) -> IdentificationResponse: pass