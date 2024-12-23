from dataclasses import dataclass
from src.app.shared.periodicity import PeriodicityValidator
from src.app.shared.method import MethodValidator
from src.app.shared.authentication import AuthenticationValidator
from src.app.shared.email import EmailValidator
from src.app.shared.password import PasswordValidator

from exceptions import EmailValidationError
from exceptions import PasswordValidationError

@dataclass
class FormParams:
    
    def get_email(self, request):
        try:
            # Get data from json body request
            email = request.form.get('email')
            # Validate the name parameter
            EmailValidator.is_valid_email(email)
            return email
        except EmailValidationError as e:
            raise EmailValidationError(str(e))
    
    def get_password(self, request):
        try:
            password = request.form.get('password')
            PasswordValidator.is_valid_password(password)
            return password
        except PasswordValidationError as e:
            raise PasswordValidationError(str(e))
