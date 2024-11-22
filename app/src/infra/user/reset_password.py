import os
import hashlib
from datetime import datetime
from dataclasses import dataclass
from flask import request, jsonify
from src.infra.sqlite3 import Database
from src.app.shared.password import PasswordValidator
from src.infra.email.gmail import Sender

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
            email = request.json.get('email')
            new_password = request.json.get('new_password')
            new_password2 = request.json.get('new_password2')

            if not email or not token or not new_password or not new_password2:
                return {"message": "Token, email, new password, and confirmation are required"}, 400

            if new_password != new_password2:
                return {"message": "New passwords do not match"}, 400

            # Validate the password
            if not PasswordValidator.is_valid_password(new_password):
                return {"message": "Password must include an uppercase letter, a lowercase letter, a number, and a symbol"}, 400

            # Hash the token
            hashed_token = hashlib.sha256(token.encode()).hexdigest()

            # Initialize the database
            db = Database(os.getenv('database_name'))
            db.create_connection()

            # Verify the token
            QUERY = """
            SELECT user_id FROM password_resets WHERE token = ? AND expires_at > ?
            """
            cursor = db.conn.cursor()
            cursor.execute(QUERY, (hashed_token, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
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

            # Send the token to the user's email
            sender = Sender()
            subject = 'apilapse | new password set'
            body = 'Hello,'+'\n\n'+'A new password has been set to your account.'+'\n\n'+'Thank you,\napilapse Team'
            sender.send_email(email, subject, body)

            return {"message": "Password reset successfully."}, 200

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while resetting the password"}, 500

        finally:
            if db:
                db.close_connection()