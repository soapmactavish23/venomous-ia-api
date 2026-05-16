from src.api.models.identification.identification_request import IdentificationRequest
from src.api.models.identification.identification_response import IdentificationResponse
from src.domain.service.audio_transcription_service import AudioTranscriptionService
from src.domain.service.deepseek_service import DeepSeekService
from src.domain.service.inference_service import InferenceService


class IdentifyService:
    def __init__(self):
        self.inference_service = InferenceService()
        self.audio_transcription_service = AudioTranscriptionService()
        self.deepseek_service = DeepSeekService()

    def identify(self, request: IdentificationRequest) -> IdentificationResponse:
        image = request.get("image")
        audio = request.get("audio")
        description = request.get("description")
        animal_name = request.get("animalName")

        if image is None:
            raise ValueError("A imagem é obrigatória.")

        inferences = self.inference_service.predict_all(image)

        audio_transcription = ""

        if audio:
            audio_transcription = self.audio_transcription_service.transcribe(audio)

        deepseek_result = self.deepseek_service.analyze(
            description=description,
            animal_name=animal_name,
            audio_transcription=audio_transcription,
            inferences=inferences,
        )

        return IdentificationResponse(
            scientific_name=deepseek_result.get("scientificName", "Animal não identificado"),
            ia_description=deepseek_result.get("iaDescription", "Não foi possível gerar análise."),
            confidence=deepseek_result.get("confidence", 0.0),
            inferences=inferences,
        )