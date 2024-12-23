import os
import hashlib

from dataclasses import dataclass
from datetime import datetime

from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config

from exceptions import UserValidationError

@dataclass
class User:
    """
    Class responsible for managing the Request information in sqlite
    """
    def __init__(self):
        """
        Initialize the Database class with the database name and configuration.
        """
        # Load the configuration from the Config class
        conf = Config()
        self.config = conf.get_config()

        # Get the database name from the environment and Initialize the database
        self.db = Database(self.config['database_name'])
        self.db.create_connection()

    def create_user(self, user_uuid, account_uuid, name, email, hashed_password, hashed_token, created_at):
        """
        Create a new user
        """
        # Insert the user into the database
        QUERY = """
        INSERT INTO users (uuid, account_uuid, name, email, password, token, role, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()
        db.execute_query(QUERY, (user_uuid, account_uuid, name, email, hashed_password, hashed_token, 'admin', created_at, ''))

    def get_user_by_token(self, uuid, token):
        """
        Get the user by hashed token
        """
        # Check if the user exists and the token matches
        QUERY = """
        SELECT id, uuid, name, email FROM users WHERE uuid = ? AND token = ? AND enabled=0
        """
        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()

        # Hash the token
        hashed_token = hashlib.sha256(token.encode()).hexdigest()

        cursor = db.conn.cursor()
        cursor.execute(QUERY, (uuid, hashed_token))
        user = cursor.fetchone()

        if not user:
            raise UserValidationError("Invalid token or uuid")

        return user

    def validate_user(self, user_info):
        """
        Validate the user by user_info
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()

        # Update the user to set validated
        user_id = user_info[0]
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        QUERY = """
        UPDATE users SET enabled = 1, updated_at = ? WHERE id = ?
        """
        db.execute_query(QUERY, (updated_at, user_id,))

    def get_user_by_email(self, email, password):
        """
        Get the user by email
        """
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the user exists and the password matches
        QUERY = """
        SELECT id, uuid, name, email FROM users WHERE email = ? AND password = ? AND enabled=1
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()

        cursor = db.conn.cursor()
        cursor.execute(QUERY, (email, hashed_password))
        user = cursor.fetchone()

        return user