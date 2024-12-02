import os
import uuid
import jwt
from datetime import datetime
from dataclasses import dataclass
from flask import request, jsonify
from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config

@dataclass
class RequestDelete:
    """
    Class responsible for updating a request in the database.
    """
    def delete(self, request_uuid):
        """
        Update a request into the database.
        """
        db = None
        try:
            # Get the Access Token from the cookie
            access_token = request.cookies.get('Access-Token')

            if not access_token:
                return {"message": "Access Token is required"}, 401

            # Load the configuration from the Config class
            conf = Config()
            config = conf.get_config()

            # Get secret key from the configuration
            secret_key = config['secret_key']
            
            try:
                payload = jwt.decode(access_token, secret_key, algorithms=['HS256'])
                user_uuid = payload['user_uuid']
            except jwt.ExpiredSignatureError:
                return {"message": "Token has expired"}, 401
            except jwt.InvalidTokenError:
                return {"message": "Invalid Token"}, 401

            # Get the database name from the environment and Initialize the database
            db = Database(config['database_name'])
            db.create_connection()

            # Retrieve user information using the UUID
            QUERY = """
            SELECT account_uuid FROM users WHERE uuid = ?
            """
            cursor = db.conn.cursor()
            cursor.execute(QUERY, (user_uuid,))
            user = cursor.fetchone()

            if user:
                account_uuid = user[0]
            else:
                return {"message": "User not found"}, 404

            # Check if the account_id belongs to the request_uuid
            CHECK_QUERY = """
            SELECT * FROM requests WHERE request_uuid = ? AND account_uuid = ?
            """
            cursor = db.conn.cursor()
            cursor.execute(CHECK_QUERY, (request_uuid, account_uuid))
            request_row = cursor.fetchone()

            if not request_row:
                return {"message": "No matching request found for the given request_uuid"}, 404

            # Delete the request row
            DELETE_QUERY = """
            DELETE FROM requests WHERE request_uuid = ? AND account_uuid = ?
            """
            cursor.execute(DELETE_QUERY, (request_uuid, account_uuid))
            db.conn.commit()

            if cursor.rowcount == 0:
                return {"message": "Request not found"}, 404

            return {"message": "Request deleted successfully"}, 200

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while deleting the request"}, 500

        finally:
            if db:
                db.close_connection()
