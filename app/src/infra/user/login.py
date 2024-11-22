import os
import hashlib
import secrets
from datetime import datetime, timedelta
from dataclasses import dataclass
from flask import request, jsonify, make_response
import jwt
from src.infra.sqlite3 import Database
from src.app.shared.email import EmailValidator
from src.app.shared.password import PasswordValidator
from src.infra.email.gmail import Sender

@dataclass
class UserLogin:
    """
    Class responsible for logging in a user and returning an access token.
    """
    def login(self):
        """
        Validate user credentials and return an access token.
        """
        db = None
        try:
            # Get the database name from the environment and initialize the database
            db = Database(os.getenv('database_name'))
            db.create_connection()

            # Get data from form fields
            email = request.form.get('email')
            password = request.form.get('password')

            if not email or not password:
                return {"message": "Email and password are required"}, 400

            # Validate the password
            if not EmailValidator.is_valid_email(email):
                return {"message": "The email address provided is not valid. Please enter a valid email address."}, 400

            # Validate the password
            if not PasswordValidator.is_valid_password(password):
                return {"message": "Password must include an uppercase letter, a lowercase letter, a number, and a symbol"}, 400

            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Check if the user exists and the password matches
            QUERY = """
            SELECT id, uuid, name, email FROM users WHERE email = ? AND password = ? AND enabled=1
            """
            cursor = db.conn.cursor()
            cursor.execute(QUERY, (email, hashed_password))
            user = cursor.fetchone()

            if user:
                user_id, user_uuid, name, email = user

                # Generate an access token
                payload = {
                    'user_uuid': user_uuid,
                    'exp': datetime.utcnow() + timedelta(hours=1)
                }
                secret_key = os.getenv('SECRET_KEY', 'your_secret_key')
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
                body = 'Hello '+name+',\n\n'+'You have already logged in.'+'\n\n'+'Thank you,\napilapse Team'
                sender.send_email(to_email, subject, body)

                # Set the access token and refresh token as HTTP-only cookies
                resp = make_response(jsonify(response), 200)
                resp.set_cookie('Access-Token', access_token, httponly=True, secure=False, samesite='Lax', max_age=3600)
                resp.set_cookie('Refresh-Token', refresh_token, httponly=True, secure=False, samesite='Lax', max_age=3600*24*15)

                return resp
            else:
                return {"message": "Invalid email or password"}, 401

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while logging in the user"}, 500

        finally:
            if db:
                db.close_connection()