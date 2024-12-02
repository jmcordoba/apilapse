class AuthenticationValidator:
    """
    Class responsible for validating the authentication parameter.
    """
    @staticmethod
    def is_valid_authentication(authentication):
        """
        Validate that the authentication is one of the allowed values: 'None', 'Basic', or 'Bearer'.
        
        :param authentication: The authentication method to validate.
        :return: True if the authentication method is valid, False otherwise.
        """
        allowed_authentications = ['None', 'Basic', 'Bearer']
        return authentication in allowed_authentications
