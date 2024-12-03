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
    def test_get_users(self, mock_database):
        """
        blablabla
        """

        # Mock the database connection and methods
        mock_db_instance = mock_database.return_value
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
        self.assertEqual(result, [
            (1, "Alice", "alice@example.com"),
            (2, "Bob", "bob@example.com")
        ])

    @patch('src.infra.user.get.Database')
    def test_get_users_exception(self, mock_database):
        """
        Test the get_users method when an exception occurs.
        """

        # Mock the database connection and methods to raise an exception
        mock_db_instance = mock_database.return_value
        mock_db_instance.fetch_all.side_effect = Exception("Database error")

        # Set the environment variable for the database name
        os.environ['database_name'] = 'test_example.db'

        # Create an instance of UserGet and call get_users
        user_get = UserGet()
        result = user_get.get_users()

        # Assertions
        mock_db_instance.create_connection.assert_called_once()
        mock_db_instance.fetch_all.assert_called_once_with("SELECT * FROM users")
        mock_db_instance.close_connection.assert_called_once()
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
