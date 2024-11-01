# tests/test_api.py

from fastapi.testclient import TestClient
from src.api import app
import unittest

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_search_endpoint(self):
        response = client.post('/search', json={'text': 'Great product', 'top_k': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)
        self.assertIsInstance(response.json(), list)

    def test_generate_endpoint(self):
        response = client.post('/generate', json={'text': 'What is the best product?', 'top_k': 2})
        self.assertEqual(response.status_code, 200)
        self.assertIn('answer', response.json())

if __name__ == '__main__':
    unittest.main()
