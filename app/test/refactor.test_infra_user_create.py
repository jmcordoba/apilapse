"""
blablabla
"""
import unittest
import os
from unittest.mock import patch, MagicMock
from flask import Flask, request
from app.src.infra.user.delete_create import UserCreate

class TestUserCreate(unittest.TestCase):
    """
    Test cases for the UserCreate class.
    """

    @patch('src.infra.user.create.Database')
    def test_insert_user(self, mock_database):
        """
        Test the insert_user method.
        """

        # Create a Flask application context
        app = Flask(__name__)
        with app.app_context():
            with app.test_request_context(json={'name': 'Alice', 'email': 'alice@example.com'}):
                # Mock the database connection and methods
                mock_db_instance = mock_database.return_value

                # Set the environment variable for the database name
                os.environ['database_name'] = 'test_example.db'

                # Create an instance of UserCreate and call insert_user
                user_create = UserCreate()
                result = user_create.insert_user()

                # Assertions
                mock_db_instance.create_connection.assert_called_once()
                mock_db_instance.execute_query.assert_called_once_with(
                    "INSERT INTO users (name, email) VALUES (?, ?)", ('Alice', 'alice@example.com')
                )
                mock_db_instance.close_connection.assert_called_once()
                self.assertEqual(result, "Database initialized and new row inserted")

    @patch('src.infra.user.create.Database')
    def test_insert_user_exception(self, mock_database):
        """
        Test the insert_user method when an exception occurs.
        """

        # Create a Flask application context
        app = Flask(__name__)
        with app.app_context():
            with app.test_request_context(json={'name': 'Alice', 'email': 'alice@example.com'}):
                # Mock the database connection and methods to raise an exception
                mock_db_instance = mock_database.return_value
                mock_db_instance.execute_query.side_effect = Exception("Database error")

                # Set the environment variable for the database name
                os.environ['database_name'] = 'test_example.db'

                # Create an instance of UserCreate and call insert_user
                user_create = UserCreate()
                result = user_create.insert_user()

                # Assertions
                mock_db_instance.create_connection.assert_called_once()
                mock_db_instance.execute_query.assert_called_once_with(
                    "INSERT INTO users (name, email) VALUES (?, ?)", ('Alice', 'alice@example.com')
                )
                mock_db_instance.close_connection.assert_called_once()
                self.assertEqual(result, "An error occurred while inserting the user")

if __name__ == "__main__":
    unittest.main()
