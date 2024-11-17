"""
blablabla
"""
import os
import sqlite3
from dataclasses import dataclass
from src.infra.sqlite3 import Database  # Import the Database class

@dataclass
class UserGet:
    """
    Retrieve all users from the database.
    """
    def get_users(self):
        """
        Retrieve all users from the database.
        """
        try:
            # Get the database name from the environment and initialize the database
            db = Database(os.getenv('database_name'))
            db.create_connection()

            # Read all rows
            rows = db.fetch_all("SELECT * FROM users")

            # Return the content of the rows
            return rows

        except sqlite3.Error as e:
            print(f"SQLite error occurred: {e}")
            return None

        finally:
            if db:
                db.close_connection()
