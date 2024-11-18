from flask import Blueprint, jsonify, request, render_template
from src.infra.user.create import UserCreate
from src.infra.user.validate import UserValidate
from src.infra.user.login import UserLogin
from src.infra.user.get import UserGet
from src.infra.user.delete import UserDelete

ip = Blueprint('ip', __name__)


@ip.route("/signin", methods=['POST'])
def ip_v1_signin():
    """
    Create a new user.
    """

    user_create = UserCreate()
    response = user_create.create()

    # Ensure response is a tuple and set default status code if not provided
    if isinstance(response, tuple):
        data, status_code = response
    else:
        data = response
        status_code = 200

    return jsonify(data), status_code, {'Access-Control-Allow-Origin':'*'}

@ip.route("/login", methods=['POST'])
def login_user():
    """
    Login a user and return an access token.
    """
    user_login = UserLogin()
    response = user_login.login()
    
    # Ensure response is a tuple and set default status code if not provided
    if isinstance(response, tuple):
        data, status_code = response
        return jsonify(data), status_code, {'Access-Control-Allow-Origin': '*'}
    else:
        return response


@ip.route("/validate", methods=['GET'])
def validate_user():
    """
    Validate a user token.
    """
    user_validate = UserValidate()
    result = user_validate.validate_token()
    return jsonify(result), 200, {'Access-Control-Allow-Origin': '*'}

@ip.route("/user/<int:id>", methods=['GET'])
def ip_v1_user_by_id(id):
    """
    Retrieve a user by their ID.
    """

    user_get = UserGet()
    rows = user_get.get_user_by_id(id)

    return jsonify({"rows": rows}), 200, {'Access-Control-Allow-Origin': '*'}

@ip.route("/users", methods=['GET'])
def db_get():
    """
    Get all users from the database.
    """

    user_get = UserGet()
    rows = user_get.get_all_users()

    return jsonify({"rows": rows}), 200, {'Access-Control-Allow-Origin': '*'}

@ip.route("/user/<int:id>", methods=['DELETE'])
def delete_user(id):
    """
    Delete a user by their ID.
    """
    user_delete = UserDelete()
    message = user_delete.delete_user_by_id(id)
    return jsonify({"message": message}), 200, {'Access-Control-Allow-Origin': '*'}

@ip.route("/users", methods=['DELETE'])
def delete_all_users():
    """
    Delete all users from the database.
    """
    user_delete = UserDelete()
    message = user_delete.delete_all_users()
    return jsonify({"message": message}), 200, {'Access-Control-Allow-Origin': '*'}
