from flask import Blueprint, jsonify, request, render_template
from src.infra.user.create import UserCreate
from src.infra.user.validate import UserValidate
from src.infra.user.login import UserLogin
from src.infra.user.get import UserGet
from src.infra.user.delete import UserDelete
from src.infra.user.user_info import UserInfo
from src.infra.user.user_delete import UserRemove
from src.infra.user.change_password import UserChangePassword
from src.infra.user.request_reset_password import UserRequestPasswordReset
from src.infra.user.reset_password import UserResetPassword
from src.infra.user.logout import UserLogout

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
def ip_v1_login_user():
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
def ip_v1_validate_user():
    """
    Validate a user token.
    """
    user_validate = UserValidate()
    result = user_validate.validate_token()
    return jsonify(result), 200, {'Access-Control-Allow-Origin': '*'}

@ip.route("/me", methods=['GET'])
def ip_v1_me():
    """
    Retrieve user information using the Access Token from the cookie.
    """
    user_info = UserInfo()
    response = user_info.user_info()
    
    # Ensure response is a tuple and set default status code if not provided
    if isinstance(response, tuple):
        data, status_code = response
        print(status_code)
        print(jsonify(data))
        return jsonify(data), status_code, {'Access-Control-Allow-Origin': '*'}
    else:
        return response

@ip.route("/me", methods=['DELETE'])
def ip_v1_remove_user():
    """
    Remove a user using the Access Token or Refresh Token from the cookie.
    """
    user_remove = UserRemove()
    response = user_remove.remove_user()
    
    # Ensure response is a tuple and set default status code if not provided
    if isinstance(response, tuple):
        data, status_code = response
        return jsonify(data), status_code, {'Access-Control-Allow-Origin': '*'}
    else:
        return response

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

@ip.route("/change_password", methods=['POST'])
def change_password():
    """
    Change the user's password using the Access Token from the cookie.
    """
    user_change_password = UserChangePassword()
    response = user_change_password.change_password()
    
    # Ensure response is a tuple and set default status code if not provided
    if isinstance(response, tuple):
        data, status_code = response
        return jsonify(data), status_code, {'Access-Control-Allow-Origin': '*'}
    else:
        return response

@ip.route("/reset_password", methods=['GET'])
def request_password_reset():
    """
    Request a password reset token.
    """
    user_request_password_reset = UserRequestPasswordReset()
    response = user_request_password_reset.request_reset()
    
    # Ensure response is a tuple and set default status code if not provided
    if isinstance(response, tuple):
        data, status_code = response
        return jsonify(data), status_code, {'Access-Control-Allow-Origin': '*'}
    else:
        return response

@ip.route("/reset_password", methods=['POST'])
def reset_password():
    """
    Reset the user's password using the token.
    """
    user_reset_password = UserResetPassword()
    response = user_reset_password.reset_password()
    
    # Ensure response is a tuple and set default status code if not provided
    if isinstance(response, tuple):
        data, status_code = response
        return jsonify(data), status_code, {'Access-Control-Allow-Origin': '*'}
    else:
        return response

@ip.route("/logout", methods=['POST'])
def logout_user():
    """
    Logout a user and remove all cookies.
    """
    user_logout = UserLogout()
    response = user_logout.logout()
    
    # Ensure response is a tuple and set default status code if not provided
    if isinstance(response, tuple):
        data, status_code = response
        return jsonify(data), status_code, {'Access-Control-Allow-Origin': '*'}
    else:
        return response
