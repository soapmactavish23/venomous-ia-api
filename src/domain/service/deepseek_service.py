import os
import json
import requests
from typing import List, Optional

from dotenv import load_dotenv

from src.api.models.inference.inference_request import InferenceRequest
from src.domain.abstractions.deepseek_service_interface import DeepSeekServiceInterface

load_dotenv()

class DeepSeekService(DeepSeekServiceInterface):
    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.model = os.getenv("MODEL")

        self.allowed_animals = {
            "jararaca": {
                "animalId": 1,
                "commonName": "Jararaca",
                "scientificName": "Bothrops Jararaca"
            },
            "cascavel": {
                "animalId": 2,
                "commonName": "Cascavel",
                "scientificName": "Crotalus Durissus"
            },
            "surucucu": {
                "animalId": 3,
                "commonName": "Surucucu",
                "scientificName": "Lachesis Muta"
            },
            "coral": {
                "animalId": 4,
                "commonName": "Coral",
                "scientificName": "Micrurus Corallinus"
            }
        }

    def analyze(
        self,
        description: Optional[str],
        animal_name: Optional[str],
        audio_transcription: Optional[str],
        inferences: List[InferenceRequest],
    ) -> dict:
        prompt = self.__build_prompt(
            description=description,
            animal_name=animal_name,
            audio_transcription=audio_transcription,
            inferences=inferences,
        )

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0.1
                }
            },
            timeout=120
        )

        response.raise_for_status()

        raw_response = response.json().get("response", "{}")

        try:
            result = json.loads(raw_response)
        except json.JSONDecodeError:
            return self.__fallback_response()

        return self.__normalize_result(result)

    def __build_prompt(
        self,
        description: Optional[str],
        animal_name: Optional[str],
        audio_transcription: Optional[str],
        inferences: List[InferenceRequest],
    ) -> str:
        inferences_text = "\n".join([
            f"- {item.model_name}: animalId={item.animal_id}, animalName={item.animal_name}, confiança={item.confidence}%, tempo={item.inference_time_ms}ms"
            for item in inferences
        ])

        allowed_animals_text = json.dumps(
            list(self.allowed_animals.values()),
            ensure_ascii=False,
            indent=2
        )

        return f"""
Você é um agente multimodal de apoio à identificação de animais peçonhentos.

Tarefa:
Analise as inferências dos modelos de visão computacional, a descrição textual, a transcrição do áudio e o animal informado pelo usuário. 
Depois escolha apenas uma serpente da lista permitida.

Lista permitida:
{allowed_animals_text}

Dados recebidos:

Animal informado pelo usuário:
{animal_name or "Não informado"}

Descrição textual:
{description or "Não informada"}

Transcrição do áudio:
{audio_transcription or "Não enviada"}

Inferências dos modelos:
{inferences_text}

Regras obrigatórias:
- Escolha obrigatoriamente apenas uma serpente da lista permitida.
- Não invente outro animal.
- Não invente outro nome científico.
- O campo scientificName deve ser exatamente um dos nomes científicos da lista permitida.
- O campo commonName deve ser exatamente um dos nomes populares da lista permitida.
- O campo confidence deve ser um número entre 0 e 100.
- Use as inferências dos modelos como principal evidência.
- Use a descrição e a transcrição apenas como evidências complementares.
- Não copie literalmente a transcrição do áudio.
- Não reescreva frases confusas do usuário.
- O campo iaDescription deve conter um texto único com:
  1. identificação provável;
  2. justificativa do motivo da escolha;
  3. orientação segura ao usuário.
- Não crie os campos decisionReason ou recommendation.
- Não gere diagnóstico médico definitivo.
- Não substitua avaliação profissional.
- Retorne APENAS JSON válido.

Formato obrigatório:

{{
  "animalId": 1,
  "scientificName": "Bothrops Jararaca",
  "commonName": "Jararaca",
  "confidence": 0.0,
  "iaDescription": "Identificação provável: Jararaca. A escolha foi feita porque os modelos de visão computacional apresentaram maior consenso para essa classe e as informações fornecidas pelo usuário são compatíveis. Em caso de acidente, procure atendimento médico imediatamente e evite manipular o animal."
}}
"""

    def __normalize_result(self, result: dict) -> dict:
        selected = self.__find_selected_animal(result)

        confidence = result.get("confidence", 0.0)

        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            confidence = 0.0

        confidence = max(0.0, min(confidence, 100.0))

        ia_description = result.get("iaDescription")

        if not ia_description:
            ia_description = (
                f"Identificação provável: {selected['commonName']}. "
                f"A escolha foi feita com base nas inferências dos modelos de visão computacional "
                f"e nas informações fornecidas pelo usuário. "
                f"Em caso de acidente, procure atendimento médico imediatamente e evite manipular o animal."
            )

        return {
            "animalId": selected["animalId"],
            "scientificName": selected["scientificName"],
            "commonName": selected["commonName"],
            "confidence": round(confidence, 2),
            "iaDescription": ia_description
        }

    def __find_selected_animal(self, result: dict) -> dict:
        common_name = str(result.get("commonName", "")).strip().lower()
        scientific_name = str(result.get("scientificName", "")).strip().lower()
        animal_id = result.get("animalId")

        if common_name in self.allowed_animals:
            return self.allowed_animals[common_name]

        for animal in self.allowed_animals.values():
            if animal["scientificName"].lower() == scientific_name:
                return animal

        for animal in self.allowed_animals.values():
            if animal["animalId"] == animal_id:
                return animal

        return self.allowed_animals["jararaca"]

    def __fallback_response(self) -> dict:
        return {
            "animalId": 0,
            "scientificName": "Animal não identificado",
            "commonName": "Animal não identificado",
            "confidence": 0.0,
            "iaDescription": (
                "Não foi possível consolidar a identificação automaticamente. "
                "Em caso de acidente, procure atendimento médico imediatamente e evite manipular o animal."
            )
        }