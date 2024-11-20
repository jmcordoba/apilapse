import os
import jwt
from datetime import datetime, timedelta
from dataclasses import dataclass
from flask import request, jsonify, make_response
from src.infra.sqlite3 import Database

@dataclass
class UserInfo:
    """
    Class responsible for returning the information of a user.
    """
    def user_info(self):
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

            # Check if the access token has been revoked
            db = Database(os.getenv('database_name'))
            db.create_connection()
            # Retrieve user information using the UUID
            QUERY = """
            SELECT id, uuid, name, email, created_at, updated_at FROM users WHERE uuid = ?
            """
            cursor = db.conn.cursor()
            cursor.execute(QUERY, (user_uuid,))
            user = cursor.fetchone()

            if user:
                user_info = {
                    "id": user[0],
                    "uuid": user[1],
                    "name": user[2],
                    "email": user[3],
                    "created_at": user[4],
                    "updated_at": user[5]
                }
                # Create response
                resp = make_response(jsonify(user_info), 200)
                resp.set_cookie('Access-Token', access_token, httponly=True, secure=True, samesite='Lax')
                resp.set_cookie('Refresh-Token', refresh_token, httponly=True, secure=True, samesite='Lax')

                return resp
            else:
                return {"message": "User not found"}, 404

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while retrieving user information"}, 500

        finally:
            if db:
                db.close_connection()