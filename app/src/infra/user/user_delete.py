import jwt
from datetime import datetime
from dataclasses import dataclass
from flask import request, jsonify
from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config

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

            # Load the configuration from the Config class
            conf = Config()
            config = conf.get_config()

            # Get secret key from the configuration
            secret_key = config['secret_key']
            
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

            # Get the database name from the environment and Initialize the database
            db = Database(config['database_name'])
            db.create_connection()

            # Check if there is a user with enabled = true and get id, uuid, and account_uuid
            CHECK_QUERY = """
            SELECT id, uuid, account_uuid FROM users WHERE enabled = 1 and uuid = ?
            """
            cursor = db.conn.cursor()
            cursor.execute(CHECK_QUERY, (user_uuid,))
            user = cursor.fetchone()

            if not user:
                return {"message": "No enabled users found"}, 404

            user_id, user_uuid, account_uuid = user

            # Check if there is an account with removed = false and get account_uuid
            CHECK_QUERY = """
            SELECT account_uuid FROM accounts WHERE removed = 0 and account_uuid = ?
            """
            cursor = db.conn.cursor()
            cursor.execute(CHECK_QUERY, (account_uuid,))
            account = cursor.fetchone()

            if not account:
                return {"message": "No active accounts found"}, 404

            # Disable the user using the UUID
            UPDATE_QUERY = """
            UPDATE users SET enabled = 0 WHERE uuid = ?
            """
            cursor = db.conn.cursor()
            cursor.execute(UPDATE_QUERY, (user_uuid,))
            db.conn.commit()

            if cursor.rowcount == 0:
                return {"message": "User not found"}, 404
            
            # Update the user row with to set the updated_at field
            updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            UPDATE_QUERY = """
            UPDATE users SET updated_at = ? WHERE uuid = ?
            """
            cursor.execute(UPDATE_QUERY, (updated_at, user_uuid,))
            db.conn.commit()

            # Update the accounts table to set the removed field to true and removed_at field with the current timestamp
            UPDATE_ACCOUNT_QUERY = """
            UPDATE accounts SET removed = 1, removed_at = ? WHERE account_uuid = ?
            """
            cursor.execute(UPDATE_ACCOUNT_QUERY, (updated_at, account_uuid,))
            db.conn.commit()

            return {"message": "User disabled and account marked as removed successfully"}, 200

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while removing the user"}, 500

        finally:
            if db:
                db.close_connection()