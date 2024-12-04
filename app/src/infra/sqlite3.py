"""
blablabla
"""
import sqlite3
from sqlite3 import Error


class Database:
    """
    blablabla
    """

    def __init__(self, db_file):
        """Initialize the Database class with the database file path."""
        self.db_file = db_file
        self.conn = None

    def create_connection(self):
        """Create a database connection to the SQLite database specified by db_file."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(f"Connected to SQLite database: {self.db_file}")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        """Execute a single query."""
        if self.conn is None:
            print("Database connection is not established.")
            return None
        
        try:
            cursor = self.conn.cursor()
            if params:
                print(f"Executing query: {query} with params: {params}")
                cursor.execute(query, params)
            else:
                print(f"Executing query: {query}")
                cursor.execute(query)
            self.conn.commit()
            print("Query executed successfully.")
        except Error as e:
            print(f"Error executing query: {e}")

    def fetch_all(self, query, params=None):
        """Fetch all results from a query."""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_one(self, query, params=None):
        """Fetch a single result from a query."""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            row = cursor.fetchone()
            return row
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
