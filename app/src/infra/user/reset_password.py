import os
import hashlib
from datetime import datetime
from dataclasses import dataclass
from flask import request, jsonify
from src.infra.sqlite3 import Database

@dataclass
class UserResetPassword:
    """
    Class responsible for resetting the user's password.
    """
    def reset_password(self):
        """
        Reset the user's password using the token.
        """
        db = None
        try:
            # Get the token and new password from the json fields
            token = request.json.get('token')
            new_password = request.json.get('new_password')
            new_password2 = request.json.get('new_password2')

            print(token)

            if not token or not new_password or not new_password2:
                return {"message": "Token, new password, and confirmation are required"}, 400

            if new_password != new_password2:
                return {"message": "New passwords do not match"}, 400

            # Hash the token
            hashed_token = hashlib.sha256(token.encode()).hexdigest()

            # Initialize the database
            db = Database(os.getenv('database_name'))
            db.create_connection()

            # Verify the token
            token_query = """
            SELECT user_id FROM password_resets WHERE token = ? AND expires_at > ?
            """
            cursor = db.conn.cursor()
            cursor.execute(token_query, (hashed_token, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
            reset = cursor.fetchone()

            if not reset:
                return {"message": "Invalid or expired token"}, 401

            user_id = reset[0]

            # Hash the new password
            hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()

            # Update the password
            update_query = """
            UPDATE users SET password = ? WHERE id = ?
            """
            cursor.execute(update_query, (hashed_new_password, user_id))
            db.conn.commit()

            # Delete the used token
            delete_query = """
            DELETE FROM password_resets WHERE token = ?
            """
            cursor.execute(delete_query, (hashed_token,))
            db.conn.commit()

            return {"message": "Password reset successfully"}, 200

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while resetting the password"}, 500

        finally:
            if db:
                db.close_connection()