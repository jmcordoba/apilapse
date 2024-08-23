"""
blablabla
"""
from dataclasses import dataclass
from flask import request, has_request_context

@dataclass
class Status:
    """
    blablabla
    """
    def get_status(self, req=request):
        """
        blablabla
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
