from src.api.models.identification.identification_request import IdentificationRequest
from src.api.models.identification.identification_response import IdentificationResponse
from src.core.exception.types.generic_exception import GenericException
from src.domain.abstractions.audio_transcription_service import AudioTranscriptionServiceInterface
from src.domain.abstractions.deepseek_service_interface import DeepSeekServiceInterface
from src.domain.abstractions.identify_service_interface import IdentifyServiceInterface
from src.domain.abstractions.inference_service_interface import InferenceServiceInterface


class IdentifyService(IdentifyServiceInterface):
    def __init__(
        self,
        inference_service: InferenceServiceInterface,
        audio_transcription_service: AudioTranscriptionServiceInterface,
        deepseek_service: DeepSeekServiceInterface,
    ):
        self.__inference_service = inference_service
        self.__audio_transcription_service = audio_transcription_service
        self.__deepseek_service = deepseek_service

    def identify(self, request: IdentificationRequest) -> IdentificationResponse:
        request.validate()

        try:
            print("CNNs identifications Started.")
            inferences = self.__inference_service.predict_all(request.image)
            print("CNNs identifications Finished.")

            audio_transcription = None

            if request.audio:
                print("Audio transcription Started.")
                audio_transcription = self.__audio_transcription_service.transcribe(request.audio)
                print("Audio transcription Finished.")

            print("IA identification Started.")
            deepseek_result = self.__deepseek_service.analyze(
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

        except GenericException:
            raise

        except Exception as e:
            msg = f"Erro ao identificar animal: {str(e)}"
            print(msg)
            raise GenericException(msg)