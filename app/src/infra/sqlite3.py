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

    """
    blablabla
    """
    def create_connection(self):
        """Create a database connection to the SQLite database specified by db_file."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(f"Connected to SQLite database: {self.db_file}")
        except Error as e:
            print(f"Error connecting to database: {e}")

    """
    blablabla
    """
    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    """
    blablabla
    """
    def execute_query(self, query, params=None):
        """Execute a single query."""
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

    """
    blablabla
    """
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

# Example usage:
if __name__ == "__main__":
    db = Database("example.db")
    db.create_connection()
    
    # Create a table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER
    );
    """
    db.execute_query(create_table_query)
    
    # Insert data
    insert_query = "INSERT INTO users (name, age) VALUES (?, ?)"
    db.execute_query(insert_query, ("Alice", 30))
    
    # Fetch data
    select_query = "SELECT * FROM users"
    rows = db.fetch_all(select_query)
    for row in rows:
        print(row)
    
    db.close_connection()