import unittest
from app import app

class BasicTest(unittest.TestCase):
    def test_home(self):
        tester =app.test_client(self)
        response = tester.get('/',content_type='html/text')
        self.assertEqual(response.status_code,200)