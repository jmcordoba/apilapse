import os
import hashlib
import secrets
from datetime import datetime, timedelta
from dataclasses import dataclass
from flask import request, jsonify
from src.infra.sqlite3 import Database

@dataclass
class UserRequestPasswordReset:
    """
    Class responsible for handling password reset requests.
    """
    def request_reset(self):
        """
        Generate a password reset token and send it to the user's email.
        """
        db = None
        try:
            # Get the email from the query parameter
            email = request.args.get('email')

            if not email:
                return {"message": "Email is required"}, 400

            # Initialize the database
            db = Database(os.getenv('database_name'))
            db.create_connection()

            # Check if the user exists
            user_query = """
            SELECT id, uuid FROM users WHERE email = ?
            """
            cursor = db.conn.cursor()
            cursor.execute(user_query, (email,))
            user = cursor.fetchone()

            if not user:
                return {"message": "User not found"}, 404

            user_id, user_uuid = user

            # Remove previous tokens for the user
            delete_query = """
            DELETE FROM password_resets WHERE user_id = ?
            """
            cursor.execute(delete_query, (user_id,))
            db.conn.commit()

            # Generate a password reset token
            token = secrets.token_urlsafe(16)
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            expires_at = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

            # Store the hashed token in the database
            token_query = """
            INSERT INTO password_resets (user_id, token, expires_at)
            VALUES (?, ?, ?)
            """
            cursor.execute(token_query, (user_id, hashed_token, expires_at))
            db.conn.commit()

            # Send the token to the user's email (this part is not implemented here)
            # send_email(email, token)

            return {"token": token}, 200

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while requesting password reset"}, 500

        finally:
            if db:
                db.close_connection()