import unittest
from unittest.mock import patch
from sdxlib.client import SDXClient, SDXException


"""
Unit tests for the sdxlib library

Run from the SDXLIB parent directory Using: 
    python -m unittest discover -v tests
"""

class TestSDXClient(unittest.TestCase):

    # @patch ensures that the tests do not actually perform HTTP requests but instead test the behavior of the 'SDXClient'
    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_success(self, mock_post):
        """Checks that the 'create_l2vpn' method correctly handles a successful API call."""
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {"status": "Accepted"}

        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints=[{"port_id": "urn:sdx:port:test:1", "vlan": "100"}]
        
        response = client.create_l2vpn()

        self.assertEqual(response, {"status": "Accepted"})

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_name_length_exceeds_limit(self, mock_post):
        """Checks that the 'create_l2vpn' method correctly raises a 'ValueError' when the 'name' exceeds 50 characters. """
        client = SDXClient(base_url="http://example.com")
        client.name="This is a very long name that exceeds 50 chatacters limit"
        client.endpoints=[{"port_id":"urn:sdx:port:test:1", "vlan": "100"}]

        with self.assertRaises(ValueError) as context:
            client.create_l2vpn()

        self.assertEqual(str(context.exception), "Name must be 50 characters or fewer.")

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_name_required(self, mock_post):
        """Checks that the 'create_l2vpn' method correctly raises a 'ValueError' when the 'name' is not provided (empty string)."""
        client = SDXClient(base_url="http://example.com")
        client.endpoints=[{"port_id": "urn:sdx:port:test:1", "vlan": "100"}]

        with self.assertRaises(ValueError) as context:
            client.create_l2vpn()

        self.assertEqual(str(context.exception), "Name is required.")

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_endpoints_required(self, mock_post):
        """Checks that the endpoints list is not empty."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"

        with self.assertRaises(ValueError) as context:
            client.create_l2vpn()

        self.assertEqual(str(context.exception), "Endpoints must not be empty.")

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_failure(self, mock_post):
        """Checks that the 'create_l2vpn' method correctly handles a failure scenario where the API call returns an error response."""
        mock_post.return_value.ok = False
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = "Bad Request"

        client = SDXClient(base_url="http://example.com")
        client.name="Test L2VPN"
        client.endpoints=[{"port_id": "urn:sdx:port:test:1", "vlan": "100"}]

        with self.assertRaises(SDXException) as context:
            client.create_l2vpn()

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.message, "Bad Request")

if __name__=="__main__":
    unittest.main()