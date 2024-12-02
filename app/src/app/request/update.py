import os
import uuid
import jwt
from datetime import datetime
from dataclasses import dataclass
from flask import request, jsonify
from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config
from src.app.shared.periodicity import PeriodicityValidator
from src.app.shared.method import MethodValidator
from src.app.shared.authentication import AuthenticationValidator

@dataclass
class RequestUpdate:
    """
    Class responsible for updating a request in the database.
    """
    def update(self, request_uuid):
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
            SELECT account_uuid FROM requests WHERE request_uuid = ? AND account_uuid = ?
            """
            cursor = db.conn.cursor()
            cursor.execute(CHECK_QUERY, (request_uuid, account_uuid))
            account = cursor.fetchone()

            if not account:
                return {"message": "No matching request found for the given account_uuid and request_uuid"}, 404

            # Get data from json body request
            active = request.json.get('active')
            periodicity = request.json.get('periodicity')
            name = request.json.get('name')
            url = request.json.get('url')
            method = request.json.get('method')
            headers = request.json.get('headers')
            user_agent = request.json.get('user_agent')
            authentication = request.json.get('authentication')
            credentials = request.json.get('credentials')
            body = request.json.get('body')
            tags = request.json.get('tags')

            # Validate input data
            if not isinstance(active, bool):
                return {"message": "The 'active' parameter must be a boolean"}, 400
            
            # Validate the periodicity parameter
            if not PeriodicityValidator.is_valid_periodicity(periodicity):
                return {"message": "The 'periodicity' parameter must be 'hourly', 'daily', or 'weekly'"}, 400

            # Validate the name parameter
            if not name or name.strip() == "":
                return {"message": "The 'name' parameter must not be empty"}, 400

            # Validate the name parameter
            if not url or url.strip() == "":
                return {"message": "The 'url' parameter must not be empty"}, 400

            # Validate the method parameter
            if not MethodValidator.is_valid_method(method):
                return {"message": "The 'method' parameter must be 'GET', 'POST', 'PUT', or 'DELETE'"}, 400

            # Validate the authentication parameter
            if not AuthenticationValidator.is_valid_authentication(authentication):
                return {"message": "The 'authentication' parameter must be 'None', 'Basic', or 'Bearer'"}, 400

            # Generate dates
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated_at = created_at
            
            UPDATE_QUERY = """
            UPDATE requests SET active = ?, periodicity = ?, name = ?, url = ?, method = ?, headers = ?, user_agent = ?, authentication = ?, credentials = ?, body = ?, tags = ?, updated_at = ? WHERE request_uuid = ?
            """
            cursor.execute(UPDATE_QUERY, (active, periodicity, name, url, method, headers, user_agent, authentication, credentials, body, tags, updated_at, request_uuid))
            db.conn.commit()

            data={
                "message": "Request updated successfully",
                "request_uuid": request_uuid
            }

            return data, 200

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while updating the request"}, 500

        finally:
            if db:
                db.close_connection()