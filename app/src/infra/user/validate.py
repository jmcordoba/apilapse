import os
import hashlib
from datetime import datetime
from dataclasses import dataclass
from flask import request
from src.infra.sqlite3 import Database
from src.infra.email.gmail import Sender
from src.infra.shared.conf import Config

@dataclass
class UserValidate:
    """
    Class responsible for validating a user token.
    """
    def validate_token(self):
        """
        Validate the token received as a JSON body parameter and set the user as validated.
        """
        db = None
        try:
            # Load the configuration from the Config class
            conf = Config()
            config = conf.get_config()

            # Get the database name from the environment and Initialize the database
            db = Database(config['database_name'])
            db.create_connection()

            # Get data from json body request
            uuid = request.args.get('uuid')
            token = request.args.get('token')

            if not uuid or not token:
                return {"message": "Email and token are required"}, 400

            # Hash the token
            hashed_token = hashlib.sha256(token.encode()).hexdigest()

            # Check if the user exists and the token matches
            QUERY = """
            SELECT id, uuid, name, email FROM users WHERE uuid = ? AND token = ? AND enabled=0
            """
            cursor = db.conn.cursor()
            cursor.execute(QUERY, (uuid, hashed_token))
            user = cursor.fetchone()

            if not user:
                return {"message": "Invalid token or uuid"}, 400
            
            # Update the user to set validated
            user_id = user[0]
            user_uuid = user[1]
            name = user[2]
            email = user[3]
            updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_query = """
            UPDATE users SET enabled = 1, updated_at = ? WHERE id = ?
            """
            cursor.execute(update_query, (updated_at, user_id))
            db.conn.commit()

            # Send email to the customer to welcome
            sender = Sender()
            subject = 'apilapse | welcome'
            body = 'Hello '+name+','+'\n\n'+'Welcome to apilapse!'+'\n\n'+'Thank you,\napilapse Team'
            sender.send_email(email, subject, body)

            return {"message": "User validated successfully", "user_uuid": user_uuid}, 200
                

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while validating the user"}, 400

        finally:
            if db:
                db.close_connection()