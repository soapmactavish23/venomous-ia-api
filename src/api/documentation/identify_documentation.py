from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage


def create_identify_parser():
    parser = reqparse.RequestParser()

    parser.add_argument("image", type=FileStorage, location="files", required=True)
    parser.add_argument("audio", type=FileStorage, location="files", required=False)
    parser.add_argument("description", type=str, location="form", required=False)
    parser.add_argument("animalName", type=str, location="form", required=False)

    return parser


def create_identification_response_model(namespace):
    inference_model = namespace.model("InferenceResponse", {
        "modelName": fields.String(example="MobileNetV2"),
        "confidence": fields.Float(example=0.94),
        "inferenceTimeMs": fields.Integer(example=230),
        "startedAt": fields.String(example="2026-05-11T18:30:00"),
        "finishedAt": fields.String(example="2026-05-11T18:30:01"),
        "animalId": fields.Integer(example=1),
    })

    return namespace.model("IdentificationResponse", {
        "scientificName": fields.String(example="Bothrops atrox"),
        "iaDescription": fields.String(example="Animal possivelmente peçonhento identificado pela IA."),
        "confidence": fields.Float(example=0.94),
        "inferences": fields.List(fields.Nested(inference_model))
    })