from flask import Blueprint, jsonify, request, render_template, make_response
from src.app.user.create import UserCreate
from src.app.user.validate import UserValidate
from src.app.user.login import UserLogin
from src.app.user.logout import UserLogout
from src.app.user.delete import UserDelete
from src.app.user.change_password import UserChangePassword
from src.app.user.info import Me
from src.app.user.user_remove import UserRemove
from src.app.user.user_get import UserGet

from exceptions import UserValidationError, EmailValidationError, PasswordValidationError

ip = Blueprint('ip', __name__)

@ip.route("/signin", methods=['POST'])
def ip_v1_signin():
    """
    Create a new user.
    """
    try:
        user_create = UserCreate()
        response = user_create.create(request)
        return jsonify(response), 201, {'Access-Control-Allow-Origin':'*'}
    except UserValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except EmailValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except PasswordValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except Exception as e:
        return jsonify({"message": str(e)}), 500, {'Access-Control-Allow-Origin':'*'}


@ip.route("/login", methods=['POST'])
def ip_v1_login_user():
    """
    Login a user and return an access token.
    """
    try:
        user_login = UserLogin()
        response = user_login.login()

        resp = make_response(jsonify(response))
        resp.set_cookie('Access-Token', response['access_token'], httponly=True, secure=False, samesite='Lax', max_age=3600)
        resp.set_cookie('Refresh-Token', response['refresh_token'], httponly=True, secure=False, samesite='Lax', max_age=3600*24*15)
    
        return resp, 200, {'Access-Control-Allow-Origin':'*'}
    
    except UserValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except EmailValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except PasswordValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except Exception as e:
        return jsonify({"message": str(e)}), 500, {'Access-Control-Allow-Origin':'*'}


@ip.route("/validate", methods=['GET'])
def ip_v1_validate_user():
    """
    Validate a user token.
    """
    try:
        user_validate = UserValidate()
        response = user_validate.validate_token()

        return jsonify(response), 200, {'Access-Control-Allow-Origin': '*'}
         
    except UserValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except EmailValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except PasswordValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except Exception as e:
        return jsonify({"message": str(e)}), 500, {'Access-Control-Allow-Origin':'*'}
   

@ip.route("/me", methods=['GET'])
def ip_v1_me():
    """
    Retrieve user information using the Access Token from the cookie.
    """
    try:
        me = Me()
        response, access_token, refresh_token = me.info()

        # Create response
        resp = make_response(jsonify(response), 200)
        resp.set_cookie('Access-Token', access_token, httponly=True, secure=True, samesite='Lax')
        resp.set_cookie('Refresh-Token', refresh_token, httponly=True, secure=True, samesite='Lax')

        # Return the response with cookies set
        return resp, 200, {'Access-Control-Allow-Origin': '*'}

    except UserValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except EmailValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except PasswordValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except Exception as e:
        return jsonify({"message": str(e)}), 500, {'Access-Control-Allow-Origin':'*'}
   

@ip.route("/me", methods=['DELETE'])
def ip_v1_remove_user():
    """
    Remove a user using the Access Token or Refresh Token from the cookie.
    """
    try:
        user_remove = UserRemove()
        response = user_remove.remove_user()
 
        return jsonify(response), 200, {'Access-Control-Allow-Origin': '*'}

    except UserValidationError as e:
        print(f"UserValidationError: {str(e)}")
        return {"message": str(e)}, 400
    except EmailValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except PasswordValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except Exception as e:
        return jsonify({"message": str(e)}), 500, {'Access-Control-Allow-Origin':'*'}


@ip.route("/user/<int:id>", methods=['GET'])
def ip_v1_user_by_id(id):
    """
    Retrieve a user by their ID.
    """

    try:
        user_get = UserGet()
        row = user_get.get_user_by_id(id)

        return jsonify(row), 200, {'Access-Control-Allow-Origin': '*'}
    
    except UserValidationError as e:
        print(f"UserValidationError: {str(e)}")
        return {"message": str(e)}, 400
    except EmailValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except PasswordValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except Exception as e:
        return jsonify({"message": str(e)}), 500, {'Access-Control-Allow-Origin':'*'}


@ip.route("/users", methods=['GET'])
def db_get():
    """
    Get all users from the database.
    """
    try:
        user_get = UserGet()
        rows = user_get.get_all_users()
        return jsonify(rows), 200, {'Access-Control-Allow-Origin': '*'}
    except UserValidationError as e:
        return {"message": str(e)}, 400


@ip.route("/user/<int:id>", methods=['DELETE'])
def delete_user(id):
    """
    Delete a user by Id.
    """
    try:
        user_delete = UserDelete()
        message = user_delete.delete_user_by_id(id)
        return jsonify({"message": message}), 200, {'Access-Control-Allow-Origin': '*'}
    except UserValidationError as e:
        return {"message": str(e)}, 400


@ip.route("/users", methods=['DELETE'])
def delete_all_users():
    """
    Delete all users from the database.
    """
    try:
        user_delete = UserDelete()
        message = user_delete.delete_all_users()
        return jsonify({"message": message}), 200, {'Access-Control-Allow-Origin': '*'}
    except UserValidationError as e:
        return {"message": str(e)}, 400


@ip.route("/change_password", methods=['POST'])
def change_password():
    """
    Change the user's password using the Access Token from the cookie.
    """
    try:
        user_change_password = UserChangePassword()
        response = user_change_password.change_password()
        
        return jsonify(response), 200, {'Access-Control-Allow-Origin': '*'}
        
    except UserValidationError as e:
        print(f"UserValidationError: {str(e)}")
        return {"message": str(e)}, 400
    except EmailValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except PasswordValidationError as e:
        return jsonify({"message": str(e)}), 400, {'Access-Control-Allow-Origin':'*'}
    except Exception as e:
        return jsonify({"message": str(e)}), 500, {'Access-Control-Allow-Origin':'*'}


@ip.route("/logout", methods=['POST'])
def logout_user():
    """
    Logout a user and remove all cookies.
    """
    try:
        user_logout = UserLogout()
        response = user_logout.logout()
        
        return response, 200, {'Access-Control-Allow-Origin': '*'}
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500, {'Access-Control-Allow-Origin':'*'}

