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
            # Get the database name from the environment and initialize the database
            db = Database(os.getenv('database_name'))
            db.create_connection()

            # Get data from json body request
            name = request.json.get('name')
            email = request.json.get('email')
            password = request.json.get('password')
            password2 = request.json.get('password2')

            # Check if passwords match
            if password != password2:
                data = {
                    "message": "Passwords do not match"
                }
                return data, 400

            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Generate a random token
            token = secrets.token_urlsafe(16)

            # Hash the token
            hashed_token = hashlib.sha256(token.encode()).hexdigest()

            # Generate a UUID
            user_uuid = str(uuid.uuid4())

            # Generate dates
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated_at = ''
            
            QUERY = """
            INSERT INTO users (uuid, name, email, password, token, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor = db.conn.cursor()
            cursor.execute(QUERY, (user_uuid, name, email, hashed_password, hashed_token, created_at, updated_at))
            db.conn.commit()

            # Get the inserted ID
            user_id = cursor.lastrowid

            data={
                "message": "User created successfully",
                "user_uuid": user_uuid,
                "email" : email,
                "token" : token
            }

            return data, 200

        except Exception as e:
            print(f"An error occurred: {e}")
            data = {
                "message": "An error occurred while inserting the user"
            }
            return data, 500

        finally:
            if db:
                db.close_connection()
