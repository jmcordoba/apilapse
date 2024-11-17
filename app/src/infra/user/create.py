"""
blablabla
"""
import os
from dataclasses import dataclass
from flask import request
from src.infra.sqlite3 import Database  # Import the Database class

@dataclass
class UserCreate:
    """
    blablabla
    """
    def insert_user(self):
        """
        blablabla
        """

        # Get the database name from the environment and Initialize the database
        db = Database(os.getenv('database_name'))
        db.create_connection()

        # Insert a new row
        name = request.json.get('name')
        email = request.json.get('email')
        insert_query = "INSERT INTO users (name, email) VALUES (?, ?)"
        db.execute_query(insert_query, (name, email))

        # Close connection
        db.close_connection()

        return "Database initialized and new row inserted"
