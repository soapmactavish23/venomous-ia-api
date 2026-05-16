from dataclasses import dataclass
from typing import Optional
from werkzeug.datastructures import FileStorage

@dataclass
class IdentificationRequest:
    image: Optional[FileStorage] = None
    audio: Optional[FileStorage] = None
    description: Optional[str] = None
    animal_name: Optional[str] = None