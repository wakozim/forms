import unittest
from urllib.parse import urlencode

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)

class TestForms(unittest.TestCase):

    def test_user_form(self):
        params = urlencode({
            'login': 'example@test.com',
            'phone': '+7 904 888 99 99',
            'registration': '2024-12-24',
            'username': 'ivan'
        })
        response = client.post("/get_form", params=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'user') 

    def test_event_form(self):
        params = urlencode({
            'type': 'new_user',
            'data': 'user',
            'timestamp': '05.06.2024'
        })
        response = client.post("/get_form", params=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'event') 

    def test_state_form(self):
        params = urlencode({
            'type': 'new_user',
            'id': '101'
        })
        response = client.post("/get_form", params=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'state') 

    def test_unknown_form(self):
        params = urlencode({
            'app': 'main',
            'date': '01.01.2025',
            'user': 'example@test.com'
        })
        response = client.post("/get_form", params=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
                         {'app': 'text', 'date': 'date', 'user': 'email'}) 


if __name__ == '__main__':
    unittest.main()
