import os
import sqlite3
from dataclasses import dataclass
from src.infra.sqlite3 import Database

@dataclass
class UserDelete:
    """
    Class responsible for deleting a user from the database.
    """
    def delete_user_by_id(self, user_id):
        """
        Delete a user from the database by their ID.
        """
        db = None
        try:
            # Get the database name from the environment and initialize the database
            db = Database(os.getenv('database_name'))
            db.create_connection()

            # Delete the user by ID
            QUERY = "DELETE FROM users WHERE id = ?"
            cursor = db.conn.cursor()
            cursor.execute(QUERY, (user_id,))
            db.conn.commit()

            # Check if the user was deleted
            if cursor.rowcount == 0:
                return f"No user found with ID {user_id}"
            else:
                return f"User with ID {user_id} has been deleted"

        except sqlite3.Error as e:
            print(f"SQLite error occurred: {e}")
            return "An error occurred while deleting the user"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "An unexpected error occurred while deleting the user"
        finally:
            if db:
                db.close_connection()

    def delete_all_users(self):
        """
        Delete all users from the database.
        """
        db = None
        try:
            # Get the database name from the environment and initialize the database
            db = Database(os.getenv('database_name'))
            db.create_connection()

            # Delete all users
            QUERY = "DELETE FROM users"
            cursor = db.conn.cursor()
            cursor.execute(QUERY)
            db.conn.commit()

            # Check if any users were deleted
            if cursor.rowcount == 0:
                return "No users found to delete"
            else:
                return f"All users have been deleted. Total deleted: {cursor.rowcount}"

        except sqlite3.Error as e:
            print(f"SQLite error occurred: {e}")
            return "An error occurred while deleting all users"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "An unexpected error occurred while deleting all users"
        finally:
            if db:
                db.close_connection()