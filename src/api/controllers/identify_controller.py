from flask_restx import Namespace, Resource

from src.api.documentation.common_api_responses import common_api_responses
from src.api.documentation.identify_documentation import (
    create_identify_parser,
    create_identification_response_model
)
from src.api.models.identification.identification_response import IdentificationResponse
from src.core.security.basic_auth import basic_auth_required
from src.domain.service.identify_service import IdentifyService

identify_ns = Namespace(
    "identify",
    description="Identificação de animais peçonhentos"
)

identify_parser = create_identify_parser()
identification_response_model = create_identification_response_model(identify_ns)

service = IdentifyService()


@identify_ns.route("")
class IdentifyController(Resource):

    @identify_ns.expect(identify_parser)
    @identify_ns.marshal_with(identification_response_model, code=200)
    @common_api_responses(identify_ns)
    @basic_auth_required
    def post(self):
        request = identify_parser.parse_args()
        response: IdentificationResponse = service.identify(request)
        return response.to_dict(), 200