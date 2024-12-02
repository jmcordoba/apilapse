import uuid
from datetime import datetime
from dataclasses import dataclass
from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config

@dataclass
class Request:
    """
    Class responsible for managing the Request information in sqlite
    """

    def get_account_uuid_from_user_uuid(self, user_uuid):
        """
        Get the account UUID from user UUID
        """
        
        # Load the configuration from the Config class
        conf = Config()
        config = conf.get_config()

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

        return account_uuid
    
    def get_account_uuid_from_request_uuid(self, request_uuid, account_uuid):
        """
        Get the account UUID from request UUID
        """

        # Load the configuration from the Config class
        conf = Config()
        config = conf.get_config()

        # Get the database name from the environment and Initialize the database
        db = Database(config['database_name'])
        db.create_connection()

        # Check if the account_id belongs to the request_uuid
        CHECK_QUERY = """
        SELECT account_uuid FROM requests WHERE request_uuid = ? AND account_uuid = ?
        """
        cursor = db.conn.cursor()
        cursor.execute(CHECK_QUERY, (request_uuid, account_uuid))
        account = cursor.fetchone()

        return account
    
    def create_request(self, account_uuid, active, periodicity, name, url, method, headers, user_agent, authentication, credentials, body, tags):
        """
        Create a new request
        """

        # Load the configuration from the Config class
        conf = Config()
        config = conf.get_config()

        # Get the database name from the environment and Initialize the database
        db = Database(config['database_name'])
        db.create_connection()

        # Generate a UUID for the request
        request_uuid = str(uuid.uuid4())

        # Generate dates
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_at = created_at
        
        QUERY = """
        INSERT INTO requests (account_uuid, request_uuid, active, periodicity, name, url, method, headers, user_agent, authentication, credentials, body, tags, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = db.conn.cursor()
        cursor.execute(QUERY, (account_uuid, request_uuid, active, periodicity, name, url, method, headers, user_agent, authentication, credentials, body, tags, created_at, updated_at))
        db.conn.commit()

        data={
            "message": "Request created successfully",
            "request_uuid": request_uuid
        }

        return data

    def update_request(self, request_uuid, active, periodicity, name, url, method, headers, user_agent, authentication, credentials, body, tags):
        """
        Update a request
        """

        # Generate dates
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Load the configuration from the Config class
        conf = Config()
        config = conf.get_config()

        # Get the database name from the environment and Initialize the database
        db = Database(config['database_name'])
        db.create_connection()
        
        UPDATE_QUERY = """
        UPDATE requests SET active = ?, periodicity = ?, name = ?, url = ?, method = ?, headers = ?, user_agent = ?, authentication = ?, credentials = ?, body = ?, tags = ?, updated_at = ? WHERE request_uuid = ?
        """
        cursor = db.conn.cursor()
        cursor.execute(UPDATE_QUERY, (active, periodicity, name, url, method, headers, user_agent, authentication, credentials, body, tags, updated_at, request_uuid))
        db.conn.commit()

        data={
            "message": "Request updated successfully",
            "request_uuid": request_uuid
        }
        
        return data