"""
blablabla
"""
from dataclasses import dataclass
from flask import request, has_request_context

@dataclass
class Status:
    """
    The Status class is responsible for retrieving and providing status information
    from the server and the application.
    """
    def get_status(self, req=request):
        """
        Retrieves the status information from the incoming request.

        This method extracts various details from the request context, such as the request ID,
        user IP address, user agent, and HTTP method. It then constructs and returns a response
        dictionary containing this information along with a status indicator.

        Args:
            req (request): The incoming request object.

        Returns:
            dict: A dictionary containing status, request ID, user IP, user agent, and HTTP method.
        """
        request_id = ''
        if has_request_context():
            request_id = req.environ.get("HTTP_X_REQUEST_ID")
        # getting info from request
        user_ip = req.remote_addr
        user_agent = req.user_agent.string
        user_method = req.method
        # response
        response = {
            'status':'ok',
            'request_id': request_id,
            'ip': user_ip,
            'user_agent': user_agent,
            'user_method': user_method
            }
        return response
