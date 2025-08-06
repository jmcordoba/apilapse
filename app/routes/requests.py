from flask import Blueprint, jsonify, request
from src.app.request.create import RequestCreate
from src.app.request.update import RequestUpdate
from src.app.request.get import RequestGet
from src.app.request.delete import RequestDelete

from exceptions import AuthenticationValidationError

req = Blueprint('req', __name__)

@req.route("/request", methods=['POST'])
def requests_v1_create_request():
    """
    Create a new request
    """
    request_create = RequestCreate()
    response = request_create.create(request)

    if isinstance(response, tuple):
        data, status_code = response
    else:
        data = response
        status_code = 200

    return jsonify(data), status_code, {'Access-Control-Allow-Origin':'*'}

@req.route("/request/<string:request_uuid>", methods=['PUT'])
def requests_v1_update_request_by_id(request_uuid):
    """
    Update a request
    """
    request_update = RequestUpdate()
    response = request_update.update(request, request_uuid)

    if isinstance(response, tuple):
        data, status_code = response
    else:
        data = response
        status_code = 200

    return jsonify(data), status_code, {'Access-Control-Allow-Origin':'*'}

@req.route("/request/<string:request_uuid>", methods=['GET'])
def requests_v1_get_request_by_id(request_uuid):
    """
    Get request by UUID
    """
    request_get = RequestGet()
    response = request_get.get(request, request_uuid)

    if isinstance(response, tuple):
        data, status_code = response
    else:
        data = response
        status_code = 200

    return jsonify(data), status_code, {'Access-Control-Allow-Origin':'*'}

@req.route("/all", methods=['GET'])
def requests_v1_get_all():
    """
    Get request by UUID
    """
    try:
    
        request_get = RequestGet()
        response = request_get.get_all(request)

        if isinstance(response, tuple):
            data, status_code = response
        else:
            data = response
            status_code = 200

        return jsonify(data), status_code, {'Access-Control-Allow-Origin':'*'}
    except AuthenticationValidationError as e:
        return {"message": str(e)}, 400

@req.route("/request/<string:request_uuid>", methods=['DELETE'])
def requests_v1_delete_request_by_id(request_uuid):
    """
    Get request by UUID
    """
    request_delete = RequestDelete()
    response = request_delete.delete(request, request_uuid)

    if isinstance(response, tuple):
        data, status_code = response
    else:
        data = response
        status_code = 200

    return jsonify(data), status_code, {'Access-Control-Allow-Origin':'*'}
