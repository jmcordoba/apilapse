import re

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
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None
