from flask import Blueprint, jsonify, request
from src.app.request.create import RequestCreate
from src.app.request.update import RequestUpdate
from src.app.request.get import RequestGet
from src.app.request.delete import RequestDelete

from exceptions import RequestValidationError, UserValidationError, AuthenticationValidationError

req = Blueprint('req', __name__)

@req.route("/request", methods=['POST'])
def requests_v1_create_request():
    """
    Create a new request
    """

    try:
        request_create = RequestCreate()
        response = request_create.create(request)

        return jsonify(response), 201, {'Access-Control-Allow-Origin':'*'}
    
    except UserValidationError as e:
        print(f"UserValidationError: {str(e)}")
        return {"message": str(e)}, 401
    except RequestValidationError as e:
        print(f"RequestValidationError: {str(e)}")
        return {"message": str(e)}, 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500, {'Access-Control-Allow-Origin':'*'}

@req.route("/request/<string:request_uuid>", methods=['PUT'])
def requests_v1_update_request_by_id(request_uuid):
    """
    Update a request
    """

    try:
        request_update = RequestUpdate()
        response = request_update.update(request, request_uuid)

        return jsonify(response), 200, {'Access-Control-Allow-Origin':'*'}
    
    except UserValidationError as e:
        print(f"UserValidationError: {str(e)}")
        return {"message": str(e)}, 401
    except RequestValidationError as e:
        print(f"RequestValidationError: {str(e)}")
        return {"message": str(e)}, 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500, {'Access-Control-Allow-Origin':'*'}

@req.route("/request/<string:request_uuid>", methods=['GET'])
def requests_v1_get_request_by_id(request_uuid):
    """
    Get request by UUID
    """

    try:
        request_get = RequestGet()
        response = request_get.get(request, request_uuid)

        return jsonify(response), 200, {'Access-Control-Allow-Origin':'*'}
    
    except AuthenticationValidationError as e:
        print(f"AuthenticationValidationError: {str(e)}")
        return {"message": str(e)}, 401
    except UserValidationError as e:
        print(f"UserValidationError: {str(e)}")
        return {"message": str(e)}, 401
    except RequestValidationError as e:
        print(f"RequestValidationError: {str(e)}")
        return {"message": str(e)}, 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500, {'Access-Control-Allow-Origin':'*'}

@req.route("/all", methods=['GET'])
def requests_v1_get_all():
    """
    Get request by UUID
    """
    try:
    
        request_get = RequestGet()
        response = request_get.get_all(request)

        return jsonify(response), 200, {'Access-Control-Allow-Origin':'*'}
    
    except AuthenticationValidationError as e:
        print(f"AuthenticationValidationError: {str(e)}")
        return {"message": str(e)}, 401
    except UserValidationError as e:
        print(f"UserValidationError: {str(e)}")
        return {"message": str(e)}, 401
    except RequestValidationError as e:
        print(f"RequestValidationError: {str(e)}")
        return {"message": str(e)}, 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500, {'Access-Control-Allow-Origin':'*'}

@req.route("/request/<string:request_uuid>", methods=['DELETE'])
def requests_v1_delete_request_by_id(request_uuid):
    """
    Get request by UUID
    """
    try:
        request_delete = RequestDelete()
        response = request_delete.delete(request, request_uuid)

        return jsonify(response), 200, {'Access-Control-Allow-Origin':'*'}
    
    except AuthenticationValidationError as e:
        print(f"AuthenticationValidationError: {str(e)}")
        return {"message": str(e)}, 401
    except UserValidationError as e:
        print(f"UserValidationError: {str(e)}")
        return {"message": str(e)}, 401
    except RequestValidationError as e:
        print(f"RequestValidationError: {str(e)}")
        return {"message": str(e)}, 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500, {'Access-Control-Allow-Origin':'*'}
