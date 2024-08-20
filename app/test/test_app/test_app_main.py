import unittest

from src.app.main import AppMain


class TestAppMain(unittest.TestCase):

    def test_main(self):
        
        app_main = AppMain()
        
        result = app_main.main(1,1)

        self.assertIsNot(result, 1)
        self.assertIs(result, 2)


if __name__ == '__main__':
    unittest.main()