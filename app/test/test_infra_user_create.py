import unittest
import os
from unittest.mock import patch, MagicMock
from flask import Flask, request
from src.infra.user.create import UserCreate

class TestUserCreate(unittest.TestCase):

    @patch('src.infra.user.create.Database')
    def test_insert_user(self, MockDatabase):
        # Create a Flask application context
        app = Flask(__name__)
        with app.app_context():
            with app.test_request_context(json={'name': 'Alice', 'email': 'alice@example.com'}):
                # Mock the database connection and methods
                mock_db_instance = MockDatabase.return_value

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

if __name__ == "__main__":
    unittest.main()