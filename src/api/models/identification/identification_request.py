from dataclasses import dataclass
from typing import Optional


@dataclass
class IdentificationRequest:
    image: Optional[object] = None
    audio: Optional[object] = None
    description: Optional[str] = None
    animal_name: Optional[str] = None