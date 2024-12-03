import unittest
from src.app.shared.email import EmailValidator

class TestEmailValidator(unittest.TestCase):
    """
    Test cases for the EmailValidator class.
    """
    def test_valid_email(self):
        """
        Test that valid email addresses pass the validation.
        """
        valid_emails = [
            "test@example.com",
            "user.name+tag+sorting@example.com",
            "user.name@example.co.uk",
            "user_name@example.com",
            "username@example.com",
            "username@sub.example.com"
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(EmailValidator.is_valid_email(email))

    def test_invalid_email(self):
        """
        Test that invalid email addresses fail the validation.
        """
        invalid_emails = [
            "plainaddress",
            "@missingusername.com",
            "username@.com",
            "username@com",
            "username@com.",
            "username@-example.com",
            "username@example..com",
            "username@.example.com"
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(EmailValidator.is_valid_email(email))

if __name__ == "__main__":
    unittest.main()