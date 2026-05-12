from flask import Flask
from flask_restx import Api, Resource

from src.api.controllers.identify_controller import identify_ns

app = Flask(__name__)

api = Api(
    app,
    version="1.0.0",
    title="VENOMOUS IA API",
    description="Documentação da API.",
    doc="/swagger",
    prefix="/api"
)

health_ns = api.namespace(
    "Health",
    description="Verificação de disponibilidade da API"
)


@health_ns.route("")
class HealthResource(Resource):

    def get(self):
        return {
            "status": "UP",
            "message": "Venomous IA API running"
        }, 200

api.add_namespace(identify_ns, path="/identify")