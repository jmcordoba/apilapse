from flask import Blueprint, jsonify, request
from src.infra.status import Status

health = Blueprint('health', __name__)

@health.route("/v1/status", methods=['GET'])
def v1_status():
    """
    Return the status of the application
    """
    infra_status = Status()
    response = infra_status.get_status(request)
    return jsonify(response), 200, {'Access-Control-Allow-Origin': '*'}