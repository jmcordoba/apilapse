"""
blablabla
"""
import os
import hashlib
import secrets
import uuid
from datetime import datetime
from dataclasses import dataclass
from flask import request
from src.infra.sqlite3 import Database
from src.app.shared.email import EmailValidator
from src.app.shared.password import PasswordValidator
from src.infra.email.gmail import Sender
from src.infra.shared.conf import Config

@dataclass
class UserCreate:
    """
    blablabla
    """
    def create(self):
        """
        Insert a new user into the database.
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
            name = request.json.get('name')
            email = request.json.get('email')
            password = request.json.get('password')
            password2 = request.json.get('password2')

            # Validate the password
            if not EmailValidator.is_valid_email(email):
                return {"message": "The email address provided is not valid. Please enter a valid email address."}, 400

            # Check if passwords match
            if password != password2:
                return {"message": "Passwords do not match"}, 400

            # Validate the password
            if not PasswordValidator.is_valid_password(password):
                return {"message": "Password must include an uppercase letter, a lowercase letter, a number, and a symbol"}, 400

            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Generate a random token
            token = secrets.token_urlsafe(16)

            # Hash the token
            hashed_token = hashlib.sha256(token.encode()).hexdigest()

            # Generate a UUID for user
            user_uuid = str(uuid.uuid4())

            # Generate a UUID for account
            account_uuid = str(uuid.uuid4())

            # Generate dates
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated_at = ''
            removed_at = ''
            
            # Insert the user into the database
            QUERY = """
            INSERT INTO users (uuid, account_uuid, name, email, password, token, role, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor = db.conn.cursor()
            cursor.execute(QUERY, (user_uuid, account_uuid, name, email, hashed_password, hashed_token, 'admin', created_at, updated_at))
            db.conn.commit()

            # Get the inserted ID
            #user_id = cursor.lastrowid
            
            # Insert the account into the database
            QUERY = """
            INSERT INTO accounts (account_uuid, plan, periodicity, removed, created_at, updated_at, removed_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor = db.conn.cursor()
            cursor.execute(QUERY, (account_uuid, 'free', 'monthly', 0, created_at, updated_at, removed_at))
            db.conn.commit()

            # Send email to the customer to validate the account
            sender = Sender()
            subject = 'apilapse | validate account'
            body = 'Hello '+name+','+'\n\n'+'Please click on the link below to validate your account:'+'\n\n'+'http://localhost:8080/validate?token='+token+'&uuid='+user_uuid+'\n\n'+'Thank you,\napilapse Team'
            sender.send_email(email, subject, body)

            data={
                "message": "User created successfully, please check your email to validate your account.",
                "user_uuid": user_uuid,
                "email" : email,
                "token" : token
            }

            return data, 201

        except Exception as e:
            print(f"An error occurred: {e}")
            data = {
                "message": "An error occurred while inserting the user"
            }
            return data, 500

        finally:
            if db:
                db.close_connection()
