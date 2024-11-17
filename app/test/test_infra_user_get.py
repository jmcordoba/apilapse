"""
blablabla
"""
import unittest
import os
from unittest.mock import patch, MagicMock
from src.infra.sqlite3 import Database
from src.infra.user.get import UserGet

class TestUserGet(unittest.TestCase):
    """
    blablabla
    """

    @patch('src.infra.user.get.Database')
    def test_get_users(self, MockDatabase):
        """
        blablabla
        """

        # Mock the database connection and methods
        mock_db_instance = MockDatabase.return_value
        mock_db_instance.fetch_all.return_value = [
            (1, "Alice", "alice@example.com"),
            (2, "Bob", "bob@example.com")
        ]

        # Set the environment variable for the database name
        os.environ['database_name'] = 'test_example.db'

        # Create an instance of UserGet and call get_users
        user_get = UserGet()
        result = user_get.get_users()

        # Assertions
        mock_db_instance.create_connection.assert_called_once()
        mock_db_instance.fetch_all.assert_called_once_with("SELECT * FROM users")
        mock_db_instance.close_connection.assert_called_once()
        self.assertEqual(result, "Database successfully read")

if __name__ == "__main__":
    unittest.main()
