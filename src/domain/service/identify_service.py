from src.domain.service.inference_service import InferenceService

class IdentifyService:
    def __init__(self):
        self.inference_service = InferenceService()

    def identify(self, request):
        image = request.get("image")
        audio = request.get("audio")
        description = request.get("description")
        animal_name = request.get("animalName")

        # Aqui depois entram:
        if image is None:
            raise ValueError("A imagem é obrigatória.")

        inferences = self.inference_service.predict_all(image)

        # 2. processamento da imagem
        # 2.1 Checar as inferencias de todas as IAs (MobileNetV2, EfficientNetB0, RestNet50)
        # 3. processamento do áudio
        # 3.1 Transcrever o audio
        # 5. Enviar tudo para o DeepSeek
        # 6. montagem da resposta final
        # 7. Apresentar 400 para caso de mensagem de Erro
        # file_validation_service.py
        # image_inference_service.py
        # audio_transcription_service.py
        # deepseek_service.py
        # identify_service.py

        return {
            "scientificName": animal_name or "Animal não identificado",
            "iaDescription": description or "Identificação realizada com sucesso.",
            "confidence": max([item.confidence for item in inferences], default=0.0),
            "inferences": [
                {
                    "modelName": item.model_name,
                    "confidence": item.confidence,
                    "inferenceTimeMs": item.inference_time_ms,
                    "startedAt": item.started_at.isoformat(),
                    "finishedAt": item.finished_at.isoformat(),
                    "animalId": item.animal_id,
                }
                for item in inferences
            ]
        }