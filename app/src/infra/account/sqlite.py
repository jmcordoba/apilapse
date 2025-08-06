from dataclasses import dataclass
from datetime import datetime

from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config

from exceptions import AccountValidationError

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

    def get_active_account_by_uuid(self, account_uuid):

        """
        Get the active account by UUID
        """
        # Check if the account exists
        QUERY = """
        SELECT account_uuid 
        FROM accounts 
        WHERE removed = 0 and account_uuid = ?
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()

        cursor = db.conn.cursor()
        cursor.execute(QUERY, (account_uuid,))
        account = cursor.fetchone()

        if not account:
            raise AccountValidationError("Active account UUID does not exist")
        
        return account
    
    def update_account_as_removed_by_uuid(self, account_uuid):
        """
        Update the account as removed by UUID
        """

        # Update the user to set validated
        #removed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update the account as removed
        QUERY = """
        UPDATE accounts 
        SET removed = 1, removed_at = datetime('now') 
        WHERE account_uuid = ?
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()
        db.execute_query(QUERY, (account_uuid,))

    def delete_all_accounts(self):
        """
        Delete all accounts from the database
        """
        
        QUERY = """
        DELETE FROM accounts
        """

        conf = Config()
        config = conf.get_config()
        db = Database(config['database_name'])
        db.create_connection()
        db.execute_query(QUERY, ())