import re
from exceptions import EmailValidationError

class EmailValidator:
    """
    Class responsible for validating email format.
    """
    @staticmethod
    def is_valid_email(email):
        """
        Validate that the email has the correct format.
        
        :param email: The email address to validate.
        :return: True if the email format is valid, False otherwise.
        """
        email_regex = r'^(?!.*\.\.)(?!.*\.\-)(?!.*\-\.)[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise EmailValidationError("The email address provided is not valid. Please enter a valid email address.")
        return True
