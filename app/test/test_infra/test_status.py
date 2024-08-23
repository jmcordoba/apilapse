"""
blablabla
"""
import unittest
from unittest.mock import MagicMock
from dataclasses import dataclass
from src.infra.status import Status

@dataclass
class FakeRequest:
    """
    test/infra/status/fake_request
    """
    def __init__(self, method, remote_addr, user_agent):
        """
        test/infra/status/fake_request
        """
        self.method = method
        self.remote_addr = remote_addr
        self.user_agent = user_agent

class TestInfraStatus(unittest.TestCase):
    """
    test/infra/status
    """
    def test_get_status(self):
        """
        test/infra/status/test_get_status
        """
        mock_object = MagicMock()
        mock_object.user_agent = "fake_user_agent"

        fake_request = FakeRequest('get', '7.7.7.7', mock_object)

        status = Status()
        result = status.get_status(fake_request)

        self.assertIsNot(result, 1)

if __name__ == '__main__':
    unittest.main()
