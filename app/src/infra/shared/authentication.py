import jwt
from dataclasses import dataclass
from src.infra.shared.conf import Config

@dataclass
class Authentication:
    """
    Class responsible for managing API Authentication
    """
    def get_user_uuid_from_access_token(self, request):
        """
        Get the user UUID from the Access Token
        """
        
        # Get the Access Token from the cookie
        access_token = request.cookies.get('Access-Token')

        if not access_token:
            return {"message": "Access Token is required"}, 401

        # Load the configuration from the Config class
        conf = Config()
        config = conf.get_config()

        # Get secret key from the configuration
        secret_key = config['secret_key']
        
        try:
            payload = jwt.decode(access_token, secret_key, algorithms=['HS256'])
            user_uuid = payload['user_uuid']
        except jwt.ExpiredSignatureError:
            return {"message": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Invalid Token"}, 401

        return user_uuid