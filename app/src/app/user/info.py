import os
import jwt
from datetime import datetime, timedelta
from dataclasses import dataclass
from flask import request, jsonify, make_response
from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config
from src.infra.user.sqlite import User

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

            # Create response
            resp = make_response(jsonify(response), 200)
            resp.set_cookie('Access-Token', access_token, httponly=True, secure=True, samesite='Lax')
            resp.set_cookie('Refresh-Token', refresh_token, httponly=True, secure=True, samesite='Lax')

            return resp

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while retrieving user information"}, 500