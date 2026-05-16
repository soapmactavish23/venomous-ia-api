import pytest
from datetime import datetime
from src.api.models.identification.identification_request import IdentificationRequest
from src.api.models.identification.identification_response import IdentificationResponse
from src.api.models.inference.inference_request import InferenceRequest
from src.core.exception.models.validation_exception import ValidationException
from src.domain.service.identify_service import IdentifyService


class FakeInferenceService:
    def predict_all(self, image):
        return [
            InferenceRequest(
                model_name="MobileNetV2",
                animal_id=1,
                animal_name="Jararaca",
                confidence=95.5,
                inference_time_ms=120,
                started_at=datetime.utcnow(),
                finished_at=datetime.utcnow()
            )
        ]


class FakeAudioTranscriptionService:
    def transcribe(self, audio_file):
        return "Usuário relatou acidente com possível jararaca."


class FakeDeepSeekService:
    def analyze(self, description, animal_name, audio_transcription, inferences):
        return {
            "animalId": 1,
            "scientificName": "Bothrops Jararaca",
            "commonName": "Jararaca",
            "confidence": 95.5,
            "iaDescription": "Identificação provável: Jararaca. Procure atendimento médico."
        }


def test_should_identify_animal_successfully():
    service = IdentifyService(
        inference_service=FakeInferenceService(),
        audio_transcription_service=FakeAudioTranscriptionService(),
        deepseek_service=FakeDeepSeekService()
    )

    request = IdentificationRequest(
        image=object(),
        audio=object(),
        description="Animal marrom encontrado no quintal.",
        animal_name="jararaca"
    )

    response = service.identify(request)

    assert isinstance(response, IdentificationResponse)
    assert response.scientific_name == "Bothrops Jararaca"
    assert response.confidence == 95.5
    assert len(response.inferences) == 1


def test_should_raise_validation_exception_when_image_is_missing():
    service = IdentifyService(
        inference_service=FakeInferenceService(),
        audio_transcription_service=FakeAudioTranscriptionService(),
        deepseek_service=FakeDeepSeekService()
    )

    request = IdentificationRequest(
        image=None,
        audio=None,
        description="Animal encontrado no quintal.",
        animal_name="jararaca"
    )

    with pytest.raises(ValidationException):
        service.identify(request)