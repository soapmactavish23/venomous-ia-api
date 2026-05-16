from src.api.models.identification.identification_request import IdentificationRequest
from src.api.models.identification.identification_response import IdentificationResponse
from src.domain.service.audio_transcription_service import AudioTranscriptionService
from src.domain.service.inference_service import InferenceService

class IdentifyService:
    def __init__(self):
        self.inference_service = InferenceService()
        self.audio_transcription_service = AudioTranscriptionService()

    def identify(self, request: IdentificationRequest) -> IdentificationResponse:
        image = request.get("image")
        audio = request.get("audio")
        description = request.get("description")
        animal_name = request.get("animalName")

        # Aqui depois entram:
        if image is None:
            raise ValueError("A imagem é obrigatória.")

        inferences = self.inference_service.predict_all(image)

        audio_transcription = self.audio_transcription_service.transcribe(audio)
        # 4. Enviar tudo para o DeepSeek
        # 6. montagem da resposta final
        # 7. Apresentar 400 para caso de mensagem de Erro
        # file_validation_service.py
        # image_inference_service.py
        # audio_transcription_service.py
        # deepseek_service.py
        # identify_service.py

        return IdentificationResponse(
            scientific_name=animal_name,
            ia_description=audio_transcription,
            confidence=max([item.confidence for item in inferences], default=0.0),
            inferences=inferences,
        )