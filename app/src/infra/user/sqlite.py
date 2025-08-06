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


    def disable_user_by_uuid(self, user_uuid):
        """
        Disable the user by user_uuid
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()

        # Update the user to set validated
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        QUERY = """
        UPDATE users SET enabled = 0, updated_at = ? WHERE uuid = ?
        """
        db.execute_query(QUERY, (updated_at, user_uuid,))


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
    
    def get_user_by_uuid(self, user_uuid):

        """
        Get the user by UUID
        """
        # Check if the user exists and the password matches
        QUERY = """
        SELECT id, uuid, name, email, created_at, updated_at, account_uuid 
        FROM users 
        WHERE uuid = ? AND enabled=1
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()

        cursor = db.conn.cursor()
        cursor.execute(QUERY, (user_uuid,))
        user = cursor.fetchone()

        if not user:
            raise UserValidationError("User UUID does not exist")
        
        return user
    
        
    def get_user_by_id(self, user_id):

        """
        Get the user by ID
        """
        # Check if the user exists and the password matches
        QUERY = """
        SELECT id, uuid, name, email, created_at, updated_at, account_uuid 
        FROM users 
        WHERE id = ?
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()

        cursor = db.conn.cursor()
        cursor.execute(QUERY, (user_id,))
        user = cursor.fetchone()

        if not user:
            raise UserValidationError("User ID does not exist")
        
        # Get column names from cursor description
        column_names = [desc[0] for desc in cursor.description]
        
        # Combine column names with the user data
        user_dict = dict(zip(column_names, user))
        
        return user_dict
    

    def get_all_users(self):

        """
        Get all users
        """
        # Check if the user exists and the password matches
        QUERY = """
        SELECT * FROM users 
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()

        cursor = db.conn.cursor()
        cursor.execute(QUERY, )
        rows = cursor.fetchall()
        
        # Get column names from cursor description
        column_names = [desc[0] for desc in cursor.description]
        
        # Combine column names with rows to create a list of dictionaries
        users = [dict(zip(column_names, row)) for row in rows]
        
        #print(f"users: {users}")

        if not users:
            raise UserValidationError("Users table is empty")
        
        return users
    

    def delete_user_by_id(self, user_id):
        """
        Delete a user by their ID
        """

        # Check if the user exists and the password matches
        QUERY = """
        SELECT id FROM users WHERE id = ? AND enabled=1
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()

        user = db.fetch_one(QUERY, (user_id,))

        if not user:
            raise UserValidationError("User Id does not exist")
    
        QUERY = """
        DELETE FROM users WHERE id = ? AND enabled=1
        """
        db.execute_query(QUERY, (user_id,))

    def delete_all_users(self):
        """
        Delete all users from the database
        """

        # Check if the user exists and the password matches
        QUERY = """
        SELECT id FROM users limit 1
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()

        user = db.fetch_one(QUERY, ())

        if not user:
            raise UserValidationError("There is no users to delete")

        QUERY = """
        DELETE FROM users
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()
        
        db.execute_query(QUERY, ())
    
    def is_current_password_correct(self, user_uuid, hashed_current_password):

        # Check if the user exists and the password matches
        QUERY = """
        SELECT id FROM users WHERE uuid = ? AND password = ?
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()

        data = db.fetch_one(QUERY, (user_uuid, hashed_current_password))

        print(f"user_uuid: {user_uuid}")

        return data

    def update_current_password(self, user_uuid, hashed_new_password):

        # Update the user to set validated
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        QUERY = """
        UPDATE users SET password = ?, updated_at = ? WHERE uuid = ?
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()

        data = db.execute_query(QUERY, (hashed_new_password, updated_at, user_uuid,))

        return data