from dataclasses import dataclass

from src.infra.shared.authentication import Authentication
from src.infra.request.sqlite import Request

@dataclass
class RequestDelete:
    """
    Class responsible for updating a request in the database.
    """
    def delete(self, request, request_uuid):
        """
        Update a request into the database.
        """
        auth = Authentication()
        user_uuid = auth.get_user_uuid_from_access_token(request)

        req = Request()
        account_uuid = req.get_account_uuid_from_user_uuid(user_uuid)

        data = req.delete_request_by_request_uuid(request_uuid, account_uuid)

        return data
