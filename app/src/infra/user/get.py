"""
blablabla
"""
import os
from dataclasses import dataclass
from src.infra.sqlite3 import Database  # Import the Database class

@dataclass
class UserGet:
    """
    blablabla
    """

    def get_users(self):
        """
        blablabla
        """

        # Get the database name from the environment and Initialize the database
        db = Database(os.getenv('database_name'))
        db.create_connection()

        # Read all rows
        db.fetch_all("SELECT * FROM users")

        # Close connection
        db.close_connection()

        return "Database successfully read"
