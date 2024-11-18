"""
blablabla
"""
import os
import json
import sqlite3
from dataclasses import dataclass
from src.infra.sqlite3 import Database

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
            # Set the configuration file path
            JSON_CONFIG = 'conf/dev.json'

            # Load the configuration from file
            with open(JSON_CONFIG, 'r', encoding='utf-8') as file:
                config = json.load(file)
                for key, value in config.items():
                    os.environ[key] = value

            # Get the database name from the environment and Initialize the database
            db = Database(os.getenv('database_name'))
            db.create_connection()

            # Create a table if it doesn't exist
            QUERY = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                uuid TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                token TEXT NOT NULL,
                enabled Boolean DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
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
