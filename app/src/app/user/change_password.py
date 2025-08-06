import os
import hashlib
import jwt
from dataclasses import dataclass
from flask import request, jsonify, make_response
from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config

from src.infra.user.sqlite import User

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
                return {"message": "Access Token is required"}, 401
            
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
                    return {"message": "Refresh Token is required"}, 401

                # Validate the Refresh Token
                try:
                    refresh_payload = jwt.decode(refresh_token, secret_key, algorithms=['HS256'])
                    user_uuid = refresh_payload['user_uuid']
                except jwt.ExpiredSignatureError:
                    return {"message": "Refresh Token has expired"}, 401
                except jwt.InvalidTokenError:
                    return {"message": "Invalid Refresh Token"}, 401
            except jwt.InvalidTokenError:
                return {"message": "Invalid Access Token"}, 401



            # Get data from json fields
            current_password = request.json.get('current_password')
            new_password = request.json.get('new_password')
            new_password2 = request.json.get('new_password2')

            if not current_password or not new_password or not new_password2:
                return {"message": "Current password, new password, and confirmation are required"}, 400

            if new_password != new_password2:
                return {"message": "New passwords do not match"}, 400

            # Hash the current password
            hashed_current_password = hashlib.sha256(current_password.encode()).hexdigest()

            # Hash the new password
            hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()

            

            # Create a User instance to interact with the database
            user = User()

            # Check if the current password is correct
            data = user.is_current_password_correct(user_uuid, hashed_current_password)
            if not data:
                return {
                    "message": "Current password is incorrect",
                    "user_uuid": user_uuid}, 401
            
            # Update the user's password
            user.update_current_password(user_uuid, hashed_new_password)
            
            # Send a confirmation email
            return {
                "message": "Password changed successfully",
                "user_uuid": user_uuid}, 200    

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while changing the password"}, 500
