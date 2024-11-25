import os
import hashlib
import secrets
from datetime import datetime, timedelta
from dataclasses import dataclass
from flask import request, jsonify
from src.infra.sqlite3 import Database
from src.app.shared.email import EmailValidator
from src.infra.email.gmail import Sender
from src.infra.shared.conf import Config

@dataclass
class UserRequestPasswordReset:
    """
    Class responsible for handling password reset requests.
    """
    def request_reset(self):
        """
        Generate a password reset token and send it to the user's email.
        """
        db = None
        try:
            # Get the email from the query parameter
            email = request.args.get('email')

            if not email:
                return {"message": "Email is required"}, 400

            # Validate the password
            if not EmailValidator.is_valid_email(email):
                return {"message": "The email address provided is not valid. Please enter a valid email address."}, 400

            # Load the configuration from the Config class
            conf = Config()
            config = conf.get_config()

            # Get the database name from the environment and Initialize the database
            db = Database(config['database_name'])
            db.create_connection()

            # Check if the user exists
            user_query = """
            SELECT id, uuid, name FROM users WHERE email = ?
            """
            cursor = db.conn.cursor()
            cursor.execute(user_query, (email,))
            user = cursor.fetchone()

            if not user:
                return {"message": "User not found"}, 404

            user_id, user_uuid, name = user

            # Remove previous tokens for the user
            delete_query = """
            DELETE FROM password_resets WHERE user_id = ?
            """
            cursor.execute(delete_query, (user_id,))
            db.conn.commit()

            # Generate a password reset token
            token = secrets.token_urlsafe(16)
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            expires_at = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

            # Store the hashed token in the database
            QUERY = """
            INSERT INTO password_resets (user_id, token, expires_at)
            VALUES (?, ?, ?)
            """
            cursor.execute(QUERY, (user_id, hashed_token, expires_at))
            db.conn.commit()

            # Send the token to the user's email
            sender = Sender()
            subject = 'apilapse | set a new password'
            body = 'Hello '+name+',\n\n'+'Click to the following link to set a new password for your account:\n\n'+'http://localhost:8080/reset_password?token='+token+'&email='+email+'\n\n'+'If you did not request a password reset, please ignore this email.\n\n'+'Thank you,\napilapse Team'
            sender.send_email(email, subject, body)

            #return {"token": token}, 200
            return {"message": "Password reset successfully, please check your email to define a new password for your account."}, 200

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while requesting password reset"}, 500

        finally:
            if db:
                db.close_connection()