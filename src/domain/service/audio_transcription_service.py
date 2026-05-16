import tempfile
from pathlib import Path
from typing import Optional

import speech_recognition as sr
from pydub import AudioSegment
from werkzeug.datastructures import FileStorage

from src.core.exception.types.storage_exception import StorageException
from src.domain.abstractions.audio_transcription_service import AudioTranscriptionServiceInterface


class AudioTranscriptionService(AudioTranscriptionServiceInterface):

    def transcribe(self, audio_file: Optional[FileStorage]) -> Optional[str]:
        if audio_file is None:
            return None

        try:
            wav_path = self.__convert_to_wav(audio_file)

            recognizer = sr.Recognizer()

            with sr.AudioFile(str(wav_path)) as source:
                audio_data = recognizer.record(source)

            return recognizer.recognize_google(
                audio_data,
                language="pt-BR"
            )

        except sr.UnknownValueError:
            return "Não foi possível compreender o áudio."

        except sr.RequestError:
            raise StorageException("Não foi possível acessar o serviço de transcrição.")

        except Exception as error:
            raise StorageException(f"Erro ao processar o áudio: {str(error)}")

    def __convert_to_wav(self, audio_file: FileStorage) -> Path:
        try:
            suffix = Path(audio_file.filename or "audio").suffix or ".wav"

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_input:
                audio_file.save(temp_input.name)
                input_path = Path(temp_input.name)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_output:
                output_path = Path(temp_output.name)

            audio = AudioSegment.from_file(input_path)
            audio = audio.set_channels(1).set_frame_rate(16000)
            audio.export(output_path, format="wav")

            return output_path

        except Exception as error:
            raise StorageException(f"Erro ao converter áudio para WAV: {str(error)}")