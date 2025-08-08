import os
import jwt
from datetime import datetime, timedelta
from dataclasses import dataclass
from flask import request, jsonify, make_response
from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config
from src.infra.user.sqlite import User

from exceptions import UserValidationError

@dataclass
class Me:
    """
    Class responsible for returning the information of a user.
    """
    def info(self):
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



            # Create a User instance to interact with the database
            user = User()

            # Check if the current password is correct
            data = user.get_user_by_uuid(user_uuid)

            #if not data:
            #    return {"message": "User not found"}, 404

            response = {
                "id": data[0],
                "uuid": data[1],
                "name": data[2],
                "email": data[3],
                "created_at": data[4],
                "updated_at": data[5]
            }

            return response, access_token, refresh_token

        except UserValidationError as e:
            raise UserValidationError(str(e))
        except Exception as e:
            raise Exception("An error occurred while retrieving user information: {e}")