from dataclasses import dataclass
from src.app.shared.periodicity import PeriodicityValidator
from src.app.shared.method import MethodValidator
from src.app.shared.authentication import AuthenticationValidator
from src.app.shared.email import EmailValidator
from src.app.shared.password import PasswordValidator

from exceptions import EmailValidationError
from exceptions import PasswordValidationError

@dataclass
class BodyParams:
    """
    Class responsible for getting the JSON body parameters    
    """
    def get_active(self, request):
        """
        Get the 'active' parameter from the JSON body request
        """
        # Get data from json body request
        active = request.json.get('active')
        # Validate input data
        if active not in [0, 1]:
            return {
                "error": True,
                "message": "The 'active' parameter must be an integer with value 0 or 1"
            }
        return active

    def get_periodicity(self, request):
        
        # Get data from json body request
        periodicity = request.json.get('periodicity')
        # Validate the periodicity parameter
        if not PeriodicityValidator.is_valid_periodicity(periodicity):
            return {
                "message": "The 'periodicity' parameter must be 'hourly', 'daily', or 'weekly'"
            }, 400
        return periodicity

    def get_name(self, request):
        # Get data from json body request
        name = request.json.get('name')
        # Validate the name parameter
        if not name or name.strip() == "":
            return {
                "message": "The 'name' parameter must not be empty"
            }, 400
        return name

    def get_email(self, request):
        try:
            # Get data from json body request
            email = request.json.get('email')
            # Validate the name parameter
            EmailValidator.is_valid_email(email)
            return email
        except EmailValidationError as e:
            raise EmailValidationError(str(e))
    
    def get_password(self, request):
        try:
            password = request.json.get('password')
            PasswordValidator.is_valid_password(password)
            return password
        except PasswordValidationError as e:
            raise PasswordValidationError(str(e))

    def get_password2(self, request):
        password2 = request.json.get('password2')
        if not PasswordValidator.is_valid_password(password2):
            return False
        return password2

    def get_url(self, request):
        # Get data from json body request
        url = request.json.get('url')
        # Validate the name parameter
        if not url or url.strip() == "":
            return {
                "message": "The 'url' parameter must not be empty"
            }, 400
        return url

    def get_method(self, request):
        # Get data from json body request
        method = request.json.get('method')
        # Validate the method parameter
        if not MethodValidator.is_valid_method(method):
            return {
                "message": "The 'method' parameter must be 'GET', 'POST', 'PUT', or 'DELETE'"
            }, 400
        return method
        
    def get_headers(self, request):
        headers = request.json.get('headers')
        return headers
    
    def get_user_agent(self, request):
        user_agent = request.json.get('user_agent')
        return user_agent

    def get_authentication(self, request):
        # Get data from json body request
        authentication = request.json.get('authentication')
        # Validate the authentication parameter
        if not AuthenticationValidator.is_valid_authentication(authentication):
            return {
                "message": "The 'authentication' parameter must be 'None', 'Basic', or 'Bearer'"
            }, 400
        return authentication

    def get_credentials(self, request):
        credentials = request.json.get('credentials')
        return credentials

    def get_body(self, request):
        body = request.json.get('body')
        return body

    def get_tags(self, request):
        tags = request.json.get('tags')
        return tags
