from dataclasses import dataclass
from typing import Optional

from werkzeug.datastructures import FileStorage

from src.core.exception.models.object_problem import ObjectProblem
from src.core.exception.models.validation_exception import ValidationException


@dataclass
class IdentificationRequest:
    image: Optional[FileStorage] = None
    audio: Optional[FileStorage] = None
    description: Optional[str] = None
    animal_name: Optional[str] = None

    @classmethod
    def from_parser_args(cls, args: dict):
        return cls(
            image=args.get("image"),
            audio=args.get("audio"),
            description=args.get("description"),
            animal_name=args.get("animal_name")
        )

    def validate(self):
        objects = []

        if self.image is None:
            objects.append(ObjectProblem(
                name="image",
                user_message="A imagem é obrigatória."
            ))

        if self.description is None or not self.description.strip():
            objects.append(ObjectProblem(
                name="description",
                user_message="A descrição é obrigatória."
            ))

        if self.animal_name is None or not self.animal_name.strip():
            objects.append(ObjectProblem(
                name="animal_name",
                user_message="O nome do animal é obrigatório."
            ))

        if objects:
            raise ValidationException(
                "Um ou mais campos estão inválidos.",
                objects
            )