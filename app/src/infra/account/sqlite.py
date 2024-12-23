from dataclasses import dataclass

from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config

@dataclass
class Account:
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

    def create_account(self, account_uuid, plan, periodicity, created_at):
        """
        Create a new account
        """

        # Insert the account into the database
        QUERY = """
        INSERT INTO accounts (account_uuid, plan, periodicity, removed, created_at, updated_at, removed_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()
        db.execute_query(QUERY, (account_uuid, plan, periodicity, 0, created_at, '', ''))
