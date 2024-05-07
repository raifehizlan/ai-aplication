import unittest
from app import app

class TestApp(unittest.TestCase):

    # Test adding a record
    def test_add_record(self):
        # Create a test client
        with app.test_client() as client:
            # Simulate a POST request with test data
            response = client.post('/prediction', data={'data': 'Test data'})
            # Check if the response status code is 200 (OK)
            self.assertEqual(response.status_code, 200)
            # Check if the response data contains the expected result
            self.assertIn('result', response.json)
            # You can add more assertions based on your specific requirements
