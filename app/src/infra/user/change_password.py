import os
import hashlib
import jwt
from dataclasses import dataclass
from flask import request, jsonify, make_response
from src.infra.sqlite3 import Database

@dataclass
class UserChangePassword:
    """
    Class responsible for changing the user's password.
    """
    def change_password(self):
        """
        Retrieve user information using the Access Token from the cookie.
        """
        db = None
        try:
            # Get the Access Token from the cookie
            access_token = request.cookies.get('Access-Token')
            refresh_token = request.cookies.get('Refresh-Token')

            if not access_token and not refresh_token:
                return {"message": "Access Token is required"}, 401
            print(access_token)
            # Validate the Access Token
            secret_key = os.getenv('SECRET_KEY', 'your_secret_key')
            print(secret_key)
            try:
                payload = jwt.decode(access_token, secret_key, algorithms=['HS256'])
                user_uuid = payload['user_uuid']

            except jwt.ExpiredSignatureError:
                if not refresh_token:
                    return {"message": "Refresh Token is required"}, 401

                # Validate the Refresh Token
                try:
                    refresh_payload = jwt.decode(refresh_token, secret_key, algorithms=['HS256'])
                    user_uuid = refresh_payload['user_uuid']
                except jwt.ExpiredSignatureError:
                    return {"message": "Refresh Token has expired"}, 401
                except jwt.InvalidTokenError:
                    return {"message": "Invalid Refresh Token"}, 401
            except jwt.InvalidTokenError:
                return {"message": "Invalid Access Token"}, 401

            # Get data from json fields
            current_password = request.json.get('current_password')
            new_password = request.json.get('new_password')
            new_password2 = request.json.get('new_password2')

            if not current_password or not new_password or not new_password2:
                return {"message": "Current password, new password, and confirmation are required"}, 400

            if new_password != new_password2:
                return {"message": "New passwords do not match"}, 400

            # Hash the current password
            hashed_current_password = hashlib.sha256(current_password.encode()).hexdigest()

            # Initialize the database
            db = Database(os.getenv('database_name'))
            db.create_connection()

            # Verify the current password
            verify_query = """
            SELECT id FROM users WHERE uuid = ? AND password = ?
            """
            cursor = db.conn.cursor()
            cursor.execute(verify_query, (user_uuid, hashed_current_password))
            user = cursor.fetchone()

            if not user:
                return {"message": "Current password is incorrect"}, 401

            # Hash the new password
            hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()

            # Update the password
            update_query = """
            UPDATE users SET password = ? WHERE uuid = ?
            """
            cursor.execute(update_query, (hashed_new_password, user_uuid))
            db.conn.commit()

            return {"message": "Password changed successfully"}, 200

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while changing the password"}, 500

        finally:
            if db:
                db.close_connection()