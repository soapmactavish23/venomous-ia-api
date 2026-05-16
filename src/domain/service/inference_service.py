import time
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List

import numpy as np
from PIL import Image
import tensorflow as tf

from src.api.models.inference.inference_request import InferenceRequest
from src.domain.abstractions.inference_service_interface import InferenceServiceInterface


class PreprocessType(Enum):
    EFFICIENTNET = "efficientnet"
    MOBILENET_V2 = "mobilenet_v2"
    RESNET_50 = "resnet_50"


class InferenceService(InferenceServiceInterface):
    def __init__(self):
        self.base_path = Path(__file__).resolve().parents[3]
        self.models_path = self.base_path / "models"
        self.labels = self.__load_labels()

        self.models = {
            "MobileNetV2": {
                "path": self.models_path / "mobilenetv2_fp16.tflite",
                "preprocess": PreprocessType.MOBILENET_V2,
            },
            "EfficientNet-B0": {
                "path": self.models_path / "efficientnetb0_fp16.tflite",
                "preprocess": PreprocessType.EFFICIENTNET,
            },
            "ResNet50": {
                "path": self.models_path / "resnet50_fp16.tflite",
                "preprocess": PreprocessType.RESNET_50,
            },
        }

        self.class_to_animal_id = {
            0: 2,  # cascavel
            1: 4,  # coral
            2: 1,  # jararaca
            3: 3,  # surucucu
        }

    def predict_all(self, image_file) -> List[InferenceRequest]:
        image = self.__load_image(image_file)
        inferences = []

        for model_name, config in self.models.items():
            inference = self.__predict(
                model_name=model_name,
                model_path=config["path"],
                preprocess_type=config["preprocess"],
                image=image
            )
            inferences.append(inference)

        return inferences

    def __predict(
        self,
        model_name: str,
        model_path: Path,
        preprocess_type: PreprocessType,
        image: Image.Image
    ) -> InferenceRequest:
        if not model_path.exists():
            raise FileNotFoundError(f"Modelo não encontrado: {model_path}")

        started_at = datetime.now()
        start_time = time.time()

        interpreter = tf.lite.Interpreter(model_path=str(model_path))
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        input_shape = input_details[0]["shape"]
        height = int(input_shape[1])
        width = int(input_shape[2])

        input_data = self.__preprocess_image(
            image=image,
            width=width,
            height=height,
            preprocess_type=preprocess_type
        )

        interpreter.set_tensor(input_details[0]["index"], input_data)
        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]["index"])[0]

        predicted_index = int(np.argmax(output_data))
        confidence = round(float(output_data[predicted_index]) * 100, 2)

        finished_at = datetime.now()
        inference_time_ms = int((time.time() - start_time) * 1000)

        return InferenceRequest(
            model_name=model_name,
            confidence=confidence,
            inference_time_ms=inference_time_ms,
            started_at=started_at,
            finished_at=finished_at,
            animal_id=self.class_to_animal_id.get(predicted_index, 0),
            animal_name=self.labels[predicted_index]
        )

    def __load_image(self, image_file) -> Image.Image:
        return Image.open(image_file.stream).convert("RGB")

    def __load_labels(self) -> List[str]:
        labels_path = self.models_path / "labels.txt"

        if not labels_path.exists():
            raise FileNotFoundError(f"Arquivo labels.txt não encontrado: {labels_path}")

        with open(labels_path, "r", encoding="utf-8") as file:
            return [
                line.strip()
                for line in file.readlines()
                if line.strip()
            ]

    def __preprocess_image(
        self,
        image: Image.Image,
        width: int,
        height: int,
        preprocess_type: PreprocessType
    ) -> np.ndarray:
        image = image.resize((width, height))
        image_array = np.array(image, dtype=np.float32)

        if preprocess_type == PreprocessType.EFFICIENTNET:
            # EfficientNetB0 com Rescaling interno: recebe 0..255
            processed = image_array

        elif preprocess_type == PreprocessType.MOBILENET_V2:
            # MobileNetV2 preprocess_input: [-1, 1]
            processed = (image_array / 127.5) - 1.0

        elif preprocess_type == PreprocessType.RESNET_50:
            # ResNet50 preprocess_input caffe:
            # RGB -> BGR e subtrai médias [103.939, 116.779, 123.68]
            bgr = image_array[..., ::-1]
            mean = np.array([103.939, 116.779, 123.68], dtype=np.float32)
            processed = bgr - mean

        else:
            raise ValueError(f"Tipo de pré-processamento inválido: {preprocess_type}")

        return np.expand_dims(processed, axis=0).astype(np.float32)