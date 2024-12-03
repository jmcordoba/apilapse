from dataclasses import dataclass

from src.infra.shared.authentication import Authentication
from src.infra.request.sqlite import Request

@dataclass
class RequestGet:
    """
    Class responsible for updating a request in the database.
    """
    def get(self, request, request_uuid):
        """
        Obtain a single request by UUID.
        """
        auth = Authentication()
        user_uuid = auth.get_user_uuid_from_access_token(request)

        req = Request()
        account_uuid = req.get_account_uuid_from_user_uuid(user_uuid)

        data = req.get_request_by_request_uuid(request_uuid, account_uuid)

        return data

    def get_all(self, request):
        """
        Obtain all requests
        """
        auth = Authentication()
        user_uuid = auth.get_user_uuid_from_access_token(request)

        req = Request()
        account_uuid = req.get_account_uuid_from_user_uuid(user_uuid)

        data = req.get_all_requests_by_account_uuid(account_uuid)
        
        return data