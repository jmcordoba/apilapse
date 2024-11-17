"""
blablabla
"""
import unittest
import os
from src.infra.sqlite3 import Database


class TestDatabase(unittest.TestCase):
    """
    test/infra/sqlite3
    """

    @classmethod
    def setUpClass(cls):
        """Set up a temporary database for testing."""
        cls.db_file = "test_example.db"
        cls.db = Database(cls.db_file)
        cls.db.create_connection()

        # Create a table for testing
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        );
        """
        cls.db.execute_query(create_table_query)

    @classmethod
    def tearDownClass(cls):
        """Close the database connection and remove the test database file."""
        cls.db.close_connection()
        os.remove(cls.db_file)

    def test_insert_and_fetch(self):
        """Test inserting and fetching data."""
        # Insert a new row
        insert_query = "INSERT INTO users (name, email) VALUES (?, ?)"
        self.db.execute_query(insert_query, ("Alice", "alice@example.com"))

        # Fetch the row
        select_query = "SELECT * FROM users WHERE name = ?"
        rows = self.db.fetch_all(select_query, ("Alice",))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "Alice")
        self.assertEqual(rows[0][2], "alice@example.com")

    def test_fetch_all(self):
        """Test fetching all rows."""
        # Insert multiple rows
        insert_query = "INSERT INTO users (name, email) VALUES (?, ?)"
        self.db.execute_query(insert_query, ("Bob", "bob@example.com"))
        self.db.execute_query(insert_query, ("Charlie", "charlie@example.com"))

        # Fetch all rows
        select_query = "SELECT * FROM users"
        rows = self.db.fetch_all(select_query)
        self.assertGreaterEqual(len(rows), 2)

    def test_create_table(self):
        """Test creating a new table."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS test_table (
            id INTEGER PRIMARY KEY,
            data TEXT NOT NULL
        );
        """
        self.db.execute_query(create_table_query)
        select_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='test_table';"
        rows = self.db.fetch_all(select_query)
        self.assertEqual(len(rows), 1)

if __name__ == "__main__":
    unittest.main()
