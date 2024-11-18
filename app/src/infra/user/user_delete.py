import os
import jwt
from dataclasses import dataclass
from flask import request, jsonify
from src.infra.sqlite3 import Database

@dataclass
class UserRemove:
    """
    Class responsible for removing a user identified by the access token or refresh token.
    """
    def remove_user(self):
        """
        Remove a user using the Access Token or Refresh Token from the cookie.
        """
        db = None
        try:
            # Get the Access Token or Refresh Token from the cookie
            access_token = request.cookies.get('Access-Token')
            refresh_token = request.cookies.get('Refresh-Token')

            if not access_token and not refresh_token:
                return {"message": "Access Token or Refresh Token is required"}, 401

            # Validate the token
            secret_key = os.getenv('SECRET_KEY', 'your_secret_key')
            try:
                if access_token:
                    payload = jwt.decode(access_token, secret_key, algorithms=['HS256'])
                else:
                    payload = jwt.decode(refresh_token, secret_key, algorithms=['HS256'])
                user_uuid = payload['user_uuid']
            except jwt.ExpiredSignatureError:
                return {"message": "Token has expired"}, 401
            except jwt.InvalidTokenError:
                return {"message": "Invalid Token"}, 401

            # Initialize the database
            db = Database(os.getenv('database_name'))
            db.create_connection()

            # Remove the user using the UUID
            delete_query = """
            DELETE FROM users WHERE uuid = ?
            """
            cursor = db.conn.cursor()
            cursor.execute(delete_query, (user_uuid,))
            db.conn.commit()

            if cursor.rowcount == 0:
                return {"message": "User not found"}, 404

            return {"message": "User removed successfully"}, 200

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while removing the user"}, 500

        finally:
            if db:
                db.close_connection()