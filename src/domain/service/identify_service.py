from numpy.f2py.auxfuncs import throw_error

from src.api.models.identification.identification_request import IdentificationRequest
from src.api.models.identification.identification_response import IdentificationResponse
from src.core.exception.api_exception_handler import handle_errors
from src.core.exception.types.generic_exception import GenericException
from src.domain.service.audio_transcription_service import AudioTranscriptionService
from src.domain.service.deepseek_service import DeepSeekService
from src.domain.service.inference_service import InferenceService


class IdentifyService:
    def __init__(self):
        self.inference_service = InferenceService()
        self.audio_transcription_service = AudioTranscriptionService()
        self.deepseek_service = DeepSeekService()

    def identify(self, request: IdentificationRequest) -> IdentificationResponse:
        request.validate()
        try:
            if request.image is None:
                raise ValueError("A imagem é obrigatória.")

            print("CNNs identifications Started.")
            inferences = self.inference_service.predict_all(request.image)
            print("CNNs identifications Finished.")

            audio_transcription = ""
            print("Audio transcription Started.")
            if request.audio:
                audio_transcription = self.audio_transcription_service.transcribe(request.audio)
            print("Audio transcription Finished.")

            print("IA identification Started.")
            deepseek_result = self.deepseek_service.analyze(
                description=request.description,
                animal_name=request.animal_name,
                audio_transcription=audio_transcription,
                inferences=inferences,
            )
            print("IA identification Finished.")

            return IdentificationResponse(
                scientific_name=deepseek_result.get("scientificName", "Animal não identificado"),
                ia_description=deepseek_result.get("iaDescription", "Não foi possível gerar análise."),
                confidence=deepseek_result.get("confidence", 0.0),
                inferences=inferences,
            )
        except ValueError as e:
            msg = "Erro ao identificar animal"
            print(msg + ": " + e.args[0])
            raise GenericException(msg)