from datetime import datetime, timedelta
from dataclasses import dataclass
from flask import request, jsonify, make_response
import jwt
from src.infra.sqlite3 import Database
from src.app.shared.email import EmailValidator
from src.app.shared.password import PasswordValidator
from src.infra.email.gmail import Sender
from src.infra.shared.conf import Config

from src.infra.user.sqlite import User

from src.infra.shared.form_params import FormParams

from exceptions import PasswordValidationError, EmailValidationError, UserValidationError

@dataclass
class UserLogin:
    """
    Class responsible for logging in a user and returning an access token.
    """
    def login(self):
        """
        Validate user credentials and return an access token.
        """

        try:
            # Load the configuration from the Config class
            conf = Config()
            config = conf.get_config()

            # Get the JSON body parameters
            form_params = FormParams()

            # Get data from form fields
            email = form_params.get_email(request)
            password = form_params.get_password(request)

            # Get the user information
            user = User()
            user_info = user.get_user_by_email_and_password(email, password)

            print(f"User info: {user_info}")

            # Validate email and password
            if user_info is None:
                raise UserValidationError("Invalid email or password")

            user_id, user_uuid, name, email = user_info

            # Generate an access token
            payload = {
                'user_uuid': user_uuid,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }
            
            # Get secret key from the configuration
            secret_key = config['secret_key']
            
            access_token = jwt.encode(payload, secret_key, algorithm='HS256')

            # Generate a refresh token
            refresh_payload = {
                'user_uuid': user_uuid,
                'exp': datetime.utcnow() + timedelta(days=15)
            }
            refresh_token = jwt.encode(refresh_payload, secret_key, algorithm='HS256')

            # Create response
            response = {
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token
            }

            # Send an email notification
            sender = Sender()
            to_email = 'jmcordoba@gmail.com'
            subject = 'apilapse | login'
            body = 'Hello '+name+',\n\n'+'You have already logged in.'+'\n\n'+'Thank you,\napilapse'
            sender.send_email(to_email, subject, body)

            return response

        except EmailValidationError as e:
            raise EmailValidationError(str(e))
        except PasswordValidationError as e:
            raise PasswordValidationError(str(e))
        except UserValidationError as e:
            raise UserValidationError(str(e))
        except Exception as e:
            raise Exception(str(e))
