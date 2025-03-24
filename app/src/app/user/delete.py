import os
import sqlite3
from dataclasses import dataclass
from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config
from src.infra.user.sqlite import User

from exceptions import UserValidationError

@dataclass
class UserDelete:
    """
    Class responsible for deleting a user from the database.
    """
    def delete_user_by_id(self, user_id):
        """
        Delete a user from the database by their ID.
        """
        try:
            # Get the user information
            user = User()
            user.delete_user_by_id(user_id)

        except UserValidationError as e:
            raise UserValidationError(str(e))

    def delete_all_users(self):
        """
        Delete all users from the database.
        """
        try:
            user = User()
            user.delete_all_users()
            return "All users deleted successfully"
        except UserValidationError as e:
            raise UserValidationError(str(e))
