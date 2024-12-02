class MethodValidator:
    """
    Class responsible for validating HTTP methods.
    """
    @staticmethod
    def is_valid_method(method):
        """
        Validate that the method is one of the allowed values: 'GET', 'POST', 'PUT', or 'DELETE'.
        
        :param method: The HTTP method to validate.
        :return: True if the method is valid, False otherwise.
        """
        allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']
        return method in allowed_methods
