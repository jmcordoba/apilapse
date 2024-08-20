"""
blablabla
"""
import unittest

from src.app.main import AppMain


class TestAppMain(unittest.TestCase):
    """
    blablabla
    """

    def test_sum(self):
        """
        blablabla
        """
        app_main = AppMain()
        result = app_main.sum(1,1)

        self.assertIsNot(result, 1)
        self.assertIs(result, 2)

    def test_min(self):
        """
        blablabla
        """
        app_main = AppMain()
        result = app_main.min(2,1)

        self.assertIsNot(result, 3)
        self.assertIs(result, 1)


if __name__ == '__main__':
    unittest.main()
