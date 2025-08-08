import os
import hashlib
import jwt
from dataclasses import dataclass
from flask import request, jsonify, make_response
from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config

from src.infra.user.sqlite import User

from exceptions import EmailValidationError, PasswordValidationError, UserValidationError

@dataclass
class UserChangePassword:
    """
    Class responsible for changing the user's password.
    """
    def change_password(self):
        """
        Retrieve user information using the Access Token from the cookie.
        """

        try:

            # Get the Access Token from the cookie
            access_token = request.cookies.get('Access-Token')
            refresh_token = request.cookies.get('Refresh-Token')

            if not access_token and not refresh_token:
                raise UserValidationError("Access Token is required")
            
            # Load the configuration from the Config class
            conf = Config()
            config = conf.get_config()

            # Get secret key from the configuration
            secret_key = config['secret_key']
            
            try:
                payload = jwt.decode(access_token, secret_key, algorithms=['HS256'])
                user_uuid = payload['user_uuid']

            except jwt.ExpiredSignatureError:
                if not refresh_token:
                    raise UserValidationError("Refresh Token is required")

                # Validate the Refresh Token
                try:
                    refresh_payload = jwt.decode(refresh_token, secret_key, algorithms=['HS256'])
                    user_uuid = refresh_payload['user_uuid']
                except jwt.ExpiredSignatureError:
                    raise UserValidationError("Refresh Token is required")
                except jwt.InvalidTokenError:
                    raise UserValidationError("Invalid Refresh Token")
            except jwt.InvalidTokenError:
                raise UserValidationError("Invalid Access Token")

            # Get data from json fields
            current_password = request.json.get('current_password')
            new_password = request.json.get('new_password')
            new_password2 = request.json.get('new_password2')

            if not current_password or not new_password or not new_password2:
                raise UserValidationError("Current password, new password, and confirmation are required")

            if new_password != new_password2:
                raise UserValidationError("New passwords do not match")

            # Hash the current password
            hashed_current_password = hashlib.sha256(current_password.encode()).hexdigest()

            # Hash the new password
            hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()

            # Create a User instance to interact with the database
            user = User()

            # Check if the current password is correct
            data = user.is_current_password_correct(user_uuid, hashed_current_password)
            if not data:
                raise UserValidationError(f"Current password is incorrect for user with uuid: {user_uuid}")
            
            # Update the user's password
            user.update_current_password(user_uuid, hashed_new_password)
            
            # Send a confirmation email
            return {
                "message": "Password changed successfully",
                "user_uuid": user_uuid}

        except UserValidationError as e:
            raise UserValidationError(str(e))
        except Exception as e:
            print(f"An error occurred: {e}")
            raise Exception("An error occurred while changing the password: {e}")
