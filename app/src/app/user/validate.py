import os
import hashlib
from datetime import datetime
from dataclasses import dataclass
from flask import request
from src.infra.sqlite3 import Database
from src.infra.email.gmail import Sender
from src.infra.shared.conf import Config

from src.infra.user.sqlite import User
from exceptions import UserValidationError, EmailValidationError

@dataclass
class UserValidate:
    """
    Class responsible for validating a user token.
    """
    def validate_token(self):
        """
        Validate the token received as a JSON body parameter and set the user as validated.
        """
        try:
            # Get data from json body request
            uuid = request.args.get('uuid')
            token = request.args.get('token')

            if not uuid or not token:
                raise EmailValidationError("Email and token are required")

            user = User()
            user_info = user.get_user_by_token(uuid, token)
            user.validate_user(user_info)

            # Update the user to set validated
            #user_id = user_info[0]
            user_uuid = user_info[1]
            name = user_info[2]
            email = user_info[3]

            # Send email to the customer to welcome
            sender = Sender()
            subject = 'apilapse | welcome'
            body = 'Hello '+name+','+'\n\n'+'Welcome to apilapse!'+'\n\n'+'Thank you,\napilapse'
            sender.send_email(email, subject, body)

            # Return the response
            data={
                "message": "User validated successfully",
                "user_uuid": user_uuid
            }
            return data

        except UserValidationError as e:
            raise UserValidationError(str(e))
        except EmailValidationError as e:
            raise EmailValidationError(str(e))
        except Exception as e:
            raise Exception(str(e))
