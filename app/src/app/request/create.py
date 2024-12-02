from dataclasses import dataclass

from src.infra.shared.authentication import Authentication
from src.infra.shared.body_params import BodyParams
from src.infra.request.sqlite import Request

@dataclass
class RequestCreate:
    """
    Class responsible for creating a new request in the database.
    """
    def create(self, request):
        """
        Insert a new request into the database.
        """
        db = None
        try:
            # Get the user UUID from the Access Token
            auth = Authentication()
            user_uuid = auth.get_user_uuid_from_access_token(request)

            # Get the user UUID from the Access Token
            req = Request()
            account_uuid = req.get_account_uuid_from_user_uuid(user_uuid)

            # Get the JSON body parameters
            body_params = BodyParams()

            active = body_params.get_active(request)
            periodicity = body_params.get_periodicity(request)
            name = body_params.get_name(request)
            url = body_params.get_url(request)
            method = body_params.get_method(request)
            headers = body_params.get_headers(request)
            user_agent = body_params.get_user_agent(request)
            authentication = body_params.get_authentication(request)
            credentials = body_params.get_credentials(request)
            body = body_params.get_body(request)
            tags = body_params.get_tags(request)
            
            # Create the request in DB
            data = req.create_request(
                account_uuid, 
                active, 
                periodicity, 
                name, 
                url, 
                method, 
                headers, 
                user_agent, 
                authentication, 
                credentials, 
                body, 
                tags)

            return data, 201

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while creating the request"}, 500

        finally:
            if db:
                db.close_connection()