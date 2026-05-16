from src.domain.service.audio_transcription_service import AudioTranscriptionService
from src.domain.service.deepseek_service import DeepSeekService
from src.domain.service.identify_service import IdentifyService
from src.domain.service.inference_service import InferenceService


def create_identify_service() -> IdentifyService:
    return IdentifyService(
        inference_service=InferenceService(),
        audio_transcription_service=AudioTranscriptionService(),
        deepseek_service=DeepSeekService()
    )