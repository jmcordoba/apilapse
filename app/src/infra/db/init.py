"""
blablabla
"""
import json
import sqlite3
from dataclasses import dataclass
from src.infra.sqlite3 import Database
from src.infra.shared.conf import Config

@dataclass
class Db:
    """
    blablabla
    """
    def init(self):
        """
        Create the database and the needed tables if they don't exist.
        """
        try:
            # Load the configuration from the Config class
            conf = Config()
            config = conf.get_config()

            # Get the database name from the environment and Initialize the database
            db = Database(config['database_name'])
            db.create_connection()

            # Create a table if it doesn't exist
            QUERY = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                uuid TEXT NOT NULL,
                account_uuid TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                token TEXT NOT NULL,
                enabled Boolean DEFAULT 0,
                role TEXT DEFAULT 'admin',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
            db.execute_query(QUERY)

            # Create the tokens table if it doesn't exist
            QUERY = """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                account_uuid TEXT NOT NULL,
                plan TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                removed Boolean DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                removed_at TEXT NOT NULL,
                FOREIGN KEY (account_uuid) REFERENCES users (account_uuid)
            );
            """
            db.execute_query(QUERY)

            # Create the tokens table if it doesn't exist
            QUERY = """
            CREATE TABLE IF NOT EXISTS tokens (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                access_token TEXT NOT NULL,
                refresh_token TEXT NOT NULL,
                created_at TEXT NOT NULL,
                access_expires_at TEXT NOT NULL,
                refresh_expires_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            """
            db.execute_query(QUERY)

            # Create the password_resets table if it doesn't exist
            QUERY = """
            CREATE TABLE IF NOT EXISTS password_resets (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                token TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            """
            db.execute_query(QUERY)

            # Close connection
            db.close_connection()
        except FileNotFoundError as e:
            print(f"Configuration file not found: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
