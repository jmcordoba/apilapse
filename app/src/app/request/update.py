from dataclasses import dataclass

from src.infra.shared.authentication import Authentication
from src.infra.shared.body_params import BodyParams
from src.infra.request.sqlite import Request

@dataclass
class RequestUpdate:
    """
    Class responsible for updating a request in the database.
    """
    def update(self, request, request_uuid):
        """
        Update a request into the database.
        """
        db = None
        try:
            # Get the user UUID from the Access Token
            auth = Authentication()
            user_uuid = auth.get_user_uuid_from_access_token(request)

            # Get the user UUID from the Access Token
            req = Request()
            account_uuid = req.get_account_uuid_from_user_uuid(user_uuid)

            # Get the account UUID from the request UUID
            account = req.get_account_uuid_from_request_uuid(request_uuid, account_uuid)
            if not account:
                return {"message": "No matching request found for the given account_uuid and request_uuid"}, 404

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
            data = req.update_request(
                request_uuid, 
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

            return data, 200

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "An error occurred while updating the request"}, 500

        finally:
            if db:
                db.close_connection()