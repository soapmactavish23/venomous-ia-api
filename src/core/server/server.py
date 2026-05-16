from flask import Flask, jsonify
from flask_restx import Api, Resource

from src.api.controllers.identify_controller import identify_ns
from src.core.exception.api_exception_handler import handle_errors

app = Flask(__name__)

authorizations = {
    "basicAuth": {
        "type": "basic"
    }
}

api = Api(
    app,
    version="1.0.0",
    title="VENOMOUS IA API",
    description="Documentação da API.",
    doc="/swagger",
    prefix="/api",
    authorizations=authorizations,
    security="basicAuth"
)


@app.errorhandler(Exception)
def global_exception_handler(error):
    problem = handle_errors(error)

    response = jsonify(problem.to_dict())
    response.status_code = problem.status

    return response


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