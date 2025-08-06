import jwt
from datetime import datetime
from dataclasses import dataclass
from flask import request, jsonify, make_response

from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config
from src.infra.user.sqlite import User
from src.infra.account.sqlite import Account

from exceptions import EmailValidationError, PasswordValidationError, UserValidationError

@dataclass
class UserRemove:
    """
    Class responsible for removing a user identified by the access token or refresh token.
    """
    def remove_user(self):
        """
        Remove a user using the Access Token or Refresh Token from the cookie.
        """

        try:
            # Get the Access Token or Refresh Token from the cookie
            access_token = request.cookies.get('Access-Token')
            refresh_token = request.cookies.get('Refresh-Token')

            if not access_token and not refresh_token:
                return {"message": "Access Token or Refresh Token is required"}, 401

            # Load the configuration from the Config class
            conf = Config()
            config = conf.get_config()

            # Get secret key from the configuration
            secret_key = config['secret_key']
            
            try:
                if access_token:
                    payload = jwt.decode(access_token, secret_key, algorithms=['HS256'])
                else:
                    payload = jwt.decode(refresh_token, secret_key, algorithms=['HS256'])
                user_uuid = payload['user_uuid']
            except jwt.ExpiredSignatureError:
                return {"message": "Token has expired"}, 401
            except jwt.InvalidTokenError:
                return {"message": "Invalid Token"}, 401


            # Create a User instance to interact with the database
            user = User()
            account = Account()

            # Check if the current password is correct
            data = user.get_user_by_uuid(user_uuid)

            user_data = {
                "id": data[0],
                "uuid": data[1],
                "name": data[2],
                "email": data[3],
                "created_at": data[4],
                "updated_at": data[5],
                "account_uuid": data[6]
            }

            account_data = account.get_active_account_by_uuid(user_data['account_uuid'])
            print("Account data: ", account_data)

            user.disable_user_by_uuid(user_data['uuid'])
            print("User disabled successfully")

            account.update_account_as_removed_by_uuid(user_data['account_uuid'])
            print("Account set as removed successfully")


            # Create response
            response = {"message": "User disabled and account marked as removed successfully"}
            resp = make_response(jsonify(response), 200)

            return resp

        except UserValidationError as e:
            print(f"An error occurred: {e}")
            return {"message": str(e)}, 401

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while removing the user"}, 500
        

