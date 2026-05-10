from flask import Blueprint

identify_routes_bp = Blueprint('identify_routes_bp', __name__)

@identify_routes_bp.route("/identify", methods=['POST'])
def identify():
    pass