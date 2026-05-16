import time
from datetime import datetime
from pathlib import Path
from typing import List

import numpy as np
from PIL import Image
from tensorflow.lite.python.interpreter import Interpreter

from src.api.models.inference.inference_request import InferenceRequest


class InferenceService:
    def __init__(self):
        base_path = Path(__file__).resolve().parents[3]

        self.models = {
            "MobileNetV2": base_path / "models" / "mobilenetv2_fp16.tflite",
            "EfficientNet-B0": base_path / "models" / "efficientnetb0_fp16.tflite",
            "ResNet50": base_path / "models" / "resnet50_fp16.tflite",
        }

        # Ajuste conforme a ordem usada no treinamento
        self.class_to_animal_id = {
            0: 1,  # cascavel
            1: 2,  # coral
            2: 3,  # jararaca
            3: 4,  # surucucu
        }

    def predict_all(self, image_file) -> List[InferenceRequest]:
        image = self.__load_image(image_file)

        inferences = []

        for model_name, model_path in self.models.items():
            inference = self.__predict(model_name, model_path, image)
            inferences.append(inference)

        return inferences

    def __predict(self, model_name: str, model_path: Path, image: Image.Image) -> InferenceRequest:
        started_at = datetime.now()
        start_time = time.time()

        interpreter = Interpreter(model_path=str(model_path))
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        input_shape = input_details[0]["shape"]
        height = input_shape[1]
        width = input_shape[2]

        input_data = self.__preprocess_image(image, width, height)

        interpreter.set_tensor(input_details[0]["index"], input_data)
        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]["index"])[0]

        predicted_index = int(np.argmax(output_data))
        confidence = float(output_data[predicted_index])

        finished_at = datetime.now()
        inference_time_ms = int((time.time() - start_time) * 1000)

        return InferenceRequest(
            model_name=model_name,
            confidence=confidence,
            inference_time_ms=inference_time_ms,
            started_at=started_at,
            finished_at=finished_at,
            animal_id=self.class_to_animal_id.get(predicted_index, 0)
        )

    def __load_image(self, image_file) -> Image.Image:
        return Image.open(image_file.stream).convert("RGB")

    def __preprocess_image(self, image: Image.Image, width: int, height: int):
        image = image.resize((width, height))

        image_array = np.array(image, dtype=np.float32)

        # Normalização padrão para modelos TensorFlow/TFLite
        image_array = image_array / 255.0

        image_array = np.expand_dims(image_array, axis=0)

        return image_array