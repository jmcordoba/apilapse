from dataclasses import dataclass

from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config

@dataclass
class User:
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

    def create_user(self, user_uuid, account_uuid, name, email, hashed_password, hashed_token, created_at):
        """
        Create a new user
        """

        # Insert the user into the database
        QUERY = """
        INSERT INTO users (uuid, account_uuid, name, email, password, token, role, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()
        #cursor = db.conn.cursor()
        #cursor.execute(QUERY, (user_uuid, account_uuid, name, email, hashed_password, hashed_token, 'admin', created_at, ''))
        db.execute_query(QUERY, (user_uuid, account_uuid, name, email, hashed_password, hashed_token, 'admin', created_at, ''))
        #db.conn.commit()
