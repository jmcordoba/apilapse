import re
from exceptions import PasswordValidationError

class PasswordValidator:
    """
    Class responsible for validating password format.
    """
    @staticmethod
    def is_valid_password(password):
        """
        Validate that the password includes an uppercase letter, a lowercase letter, a number, and a symbol.
        
        :param password: The password to validate.
        :return: True if the password format is valid, False otherwise.
        """
        if len(password) < 8:
            raise PasswordValidationError("Password must be at least 8 characters long.")

        has_uppercase = re.search(r'[A-Z]', password) is not None
        has_lowercase = re.search(r'[a-z]', password) is not None
        has_number = re.search(r'[0-9]', password) is not None
        has_symbol = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None

        if not (has_uppercase and has_lowercase and has_number and has_symbol):
            raise PasswordValidationError("Password must include an uppercase letter, a lowercase letter, a number, and a symbol.")
        
        return True
