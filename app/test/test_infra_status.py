"""
blablabla
"""
import unittest
from unittest.mock import MagicMock
from src.infra.status import Status

class TestInfraStatus(unittest.TestCase):
    """
    test/infra/status
    """
    def test_get_status(self):
        """
        test/infra/status/test_get_status
        """
        mock_user_agent = MagicMock()
        mock_user_agent.user_agent = "fake_user_agent"

        mock_request = MagicMock()
        mock_request.method = 'get'
        mock_request.remote_addr = '7.7.7.7'
        mock_request.user_agent = mock_user_agent

        status = Status()
        result = status.get_status(mock_request)

        self.assertIsNot(result, 1)

if __name__ == '__main__':
    unittest.main()
