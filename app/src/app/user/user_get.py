"""
blablabla
"""
import os
import sqlite3
from dataclasses import dataclass
from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config
from src.infra.user.sqlite import User

from exceptions import EmailValidationError, PasswordValidationError, UserValidationError

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
            # Create a User instance to interact with the database
            user = User()

            # Read all rows
            rows = user.get_all_users()

            # Return the content of the rows
            return rows

        except sqlite3.Error as e:
            print(f"SQLite error occurred: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None


    def get_user_by_id(self, id):
        """
        Retrieve a user by ID from the database.
        """
        try:
            # Create a User instance to interact with the database
            user = User()

            # Read all rows
            row = user.get_user_by_id(id)

            # Return the content of the rows
            return row

        except sqlite3.Error as e:
            print(f"SQLite error occurred: {e}")
            return None
        except UserValidationError as e:
            print(f"An error occurred: {e}")
            return {"message": str(e)}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
