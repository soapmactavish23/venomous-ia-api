from abc import ABC, abstractmethod
from typing import Optional

from werkzeug.datastructures import FileStorage

class AudioTranscriptionServiceInterface(ABC):
    @abstractmethod
    def transcribe(self, audio_file: Optional[FileStorage]) -> Optional[str]: pass