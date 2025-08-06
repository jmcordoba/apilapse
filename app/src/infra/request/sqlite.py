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
    def __init__(self):
        """
        Initialize the Database class with the database name and configuration.
        """
        # Load the configuration from the Config class
        conf = Config()
        self.config = conf.get_config()

        # Get the database name from the environment and Initialize the database
        self.db = Database(self.config['database_name'])
        self.db.create_connection()

    def get_account_uuid_from_user_uuid(self, user_uuid):
        """
        Get the account UUID from user UUID
        """

        # Retrieve user information using the UUID
        QUERY = """
        SELECT account_uuid FROM users WHERE uuid = ?
        """

        print(f"User UUID: {user_uuid}")

        # conf = Config()
        # config = conf.get_config()
        # db = Database(config['database_name'])
        # db.create_connection()

        # cursor = db.conn.cursor()
        # cursor.execute(QUERY, (user_uuid,))
        # user = cursor.fetchone()

        # if not user:
        #     raise UserValidationError("There is no users to delete")

        # print(f"User found: {user}")

        #account_uuid = user[0]

        return "hol"
    
    def get_account_uuid_from_request_uuid(self, request_uuid, account_uuid):
        """
        Get the account UUID from request UUID
        """

        # Check if the account_id belongs to the request_uuid
        CHECK_QUERY = """
        SELECT account_uuid FROM requests WHERE request_uuid = ? AND account_uuid = ?
        """
        cursor = self.db.conn.cursor()
        cursor.execute(CHECK_QUERY, (request_uuid, account_uuid))
        account = cursor.fetchone()

        return account
    
    def create_request(self, account_uuid, active, periodicity, name, url, method, headers, user_agent, authentication, credentials, body, tags):
        """
        Create a new request
        """

        # Generate a UUID for the request
        request_uuid = str(uuid.uuid4())

        # Generate dates
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_at = created_at
        
        QUERY = """
        INSERT INTO requests (account_uuid, request_uuid, active, periodicity, name, url, method, headers, user_agent, authentication, credentials, body, tags, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.db.conn.cursor()
        cursor.execute(QUERY, (account_uuid, request_uuid, active, periodicity, name, url, method, headers, user_agent, authentication, credentials, body, tags, created_at, updated_at))
        self.db.conn.commit()

        data={
            "message": "Request created successfully",
            "request_uuid": request_uuid
        }, 201

        return data

    def update_request(self, request_uuid, active, periodicity, name, url, method, headers, user_agent, authentication, credentials, body, tags):
        """
        Update a request
        """

        # Generate dates
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        UPDATE_QUERY = """
        UPDATE requests SET active = ?, periodicity = ?, name = ?, url = ?, method = ?, headers = ?, user_agent = ?, authentication = ?, credentials = ?, body = ?, tags = ?, updated_at = ? WHERE request_uuid = ?
        """
        cursor = self.db.conn.cursor()
        cursor.execute(UPDATE_QUERY, (active, periodicity, name, url, method, headers, user_agent, authentication, credentials, body, tags, updated_at, request_uuid))
        self.db.conn.commit()

        data={
            "message": "Request updated successfully",
            "request_uuid": request_uuid
        }, 200
        
        return data
    
    def get_request_by_request_uuid(self, request_uuid, account_uuid):
        """
        Get a request by request UUID
        """

        # Check if the account_id belongs to the request_uuid
        CHECK_QUERY = """
        SELECT * FROM requests WHERE request_uuid = ? AND account_uuid = ?
        """
        cursor = self.db.conn.cursor()
        cursor.execute(CHECK_QUERY, (request_uuid, account_uuid,))
        request_row = cursor.fetchone()

        if not request_row:
            return {
                "message": "No matching request found for the given request_uuid"
            }, 404

        # Convert the row to a dictionary
        columns = [column[0] for column in cursor.description]
        request_data = dict(zip(columns, request_row))

        data={
            "message": "Request obtained successfully",
            "data": request_data
        }, 200

        return data

    def get_all_requests_by_account_uuid(self, account_uuid):
        """
        Get all requests by account UUID
        """

        # Check if the account_id belongs to the request_uuid
        CHECK_QUERY = """
        SELECT * FROM requests WHERE account_uuid = ?
        """
        cursor = self.db.conn.cursor()
        cursor.execute(CHECK_QUERY, (account_uuid,))
        request_rows = cursor.fetchall()

        if not request_rows:
            return {
                "message": "No requests found for the given account_uuid"
            }, 404

        # Convert the rows to a list of dictionaries
        columns = [column[0] for column in cursor.description]
        request_data = [dict(zip(columns, row)) for row in request_rows]

        data={
            "message": "Requests obtained successfully",
            "data": request_data
        }, 200

        return data

    def delete_request_by_request_uuid(self, request_uuid, account_uuid):

        # Check if the account_id belongs to the request_uuid
        CHECK_QUERY = """
        SELECT * FROM requests WHERE request_uuid = ? AND account_uuid = ?
        """
        cursor = self.db.conn.cursor()
        cursor.execute(CHECK_QUERY, (request_uuid, account_uuid,))
        request_row = cursor.fetchone()

        if not request_row:
            return {
                "message": "No matching request found for the given request_uuid"
            }, 404

        # Delete the request row
        DELETE_QUERY = """
        DELETE FROM requests WHERE request_uuid = ? AND account_uuid = ?
        """
        cursor.execute(DELETE_QUERY, (request_uuid, account_uuid))
        self.db.conn.commit()

        if cursor.rowcount == 0:
            return {
                "message": "Request not found"
            }, 404

        data={
            "message": "Request deleted successfully"
        }, 200

        return data
