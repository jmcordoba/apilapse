"""
blablabla
"""
import os
import sqlite3
from dataclasses import dataclass
from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config

@dataclass
class UserGet:
    """
    Retrieve all users from the database.
    """
    
    def get_all_users(self):
        """
        Retrieve all users from the database.
        """
        try:
            # Load the configuration from the Config class
            conf = Config()
            config = conf.get_config()

            # Get the database name from the environment and Initialize the database
            db = Database(config['database_name'])
            db.create_connection()

            # Read all rows
            rows = db.fetch_all("SELECT * FROM users")

            # Return the content of the rows
            return rows

        except sqlite3.Error as e:
            print(f"SQLite error occurred: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        finally:
            if db:
                db.close_connection()

    def get_user_by_id(self, id):
        """
        Retrieve a user by ID from the database.
        """
        try:
            # Get the database name from the environment and initialize the database
            db = Database(os.getenv('database_name'))
            db.create_connection()

            # Read the row
            row = db.fetch_one("SELECT * FROM users WHERE id=?", (id,))

            # Return the content of the row
            return row

        except sqlite3.Error as e:
            print(f"SQLite error occurred: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        finally:
            if db:
                db.close_connection()
