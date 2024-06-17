import unittest
from unittest.mock import patch
from sdxlib.client import SDXClient, SDXException


"""
Unit tests for the sdxlib library

Run from the SDXLIB parent directory Using: 
    python -m unittest discover -v tests
"""

class TestSDXClient(unittest.TestCase):

    #### API Call Succeeds ####
    # @patch ensures that the tests do not actually perform HTTP requests but instead test the behavior of the 'SDXClient'
    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_success(self, mock_post):
        """Checks that the 'create_l2vpn' method correctly handles a successful API call."""
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {"status": "Accepted"}

        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints=[
            {"port_id": "urn:sdx:port:test:1", "vlan": "100"},
            {"port_id": "urn:sdx:port:test:1", "vlan": "200"}
        ]
        
        response = client.create_l2vpn()

        self.assertEqual(response, {"status": "Accepted"})

    #### Name Attribute ####
    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_name_required(self, mock_post):
        """Checks that the 'create_l2vpn' method correctly raises a 'ValueError' when the 'name' is not provided (empty string)."""
        client = SDXClient(base_url="http://example.com")
        client.endpoints=[
            {"port_id": "urn:sdx:port:test:1", "vlan": "100"},
            {"port_id": "urn:sdx:port:test:1", "vlan": "200"}
        ]

        with self.assertRaises(ValueError) as context:
            client.create_l2vpn()

        self.assertEqual(str(context.exception), "Name is required.")

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_name_length_exceeds_limit(self, mock_post):
        """Checks that the 'name' setter correctly raises a 'ValueError' when the 'name' exceeds 50 characters. """
        client = SDXClient(base_url="http://example.com")

        with self.assertRaises(ValueError) as context:
            client.name="This is a very long name that exceeds 50 chatacters limit"

        self.assertEqual(str(context.exception), "Name must be 50 characters or fewer.")

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_name_empty_string(self, mock_post):
        """Checks that the 'name' setter correctlys raises a 'ValueError' when the name is an empty string."""
        client = SDXClient(base_url="http://example.com")

        with self.assertRaises(ValueError) as context:
            client.name = ""

        self.assertEqual(str(context.exception), "Name cannot be an empty string.")

    #### Endpoint Attribute ####
    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_endpoints_required(self, mock_post):
        """Checks that the 'create_l2vpn' method correctly raises a 'ValueError' when the endpoints list is empty."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"

        with self.assertRaises(ValueError) as context:
            client.create_l2vpn()

        self.assertEqual(str(context.exception), "Endpoints must not be empty.")

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_endpoints_min_required(self, mock_post):
        """Checks that the 'endpoints' setter correctly raises 'ValueError' when the 'endpoints' contain less than 2 entries."""
        
        client = SDXClient(base_url="http://example.com")
        client.name="Test L2VPN"

        with self.assertRaises(ValueError) as context:
            client.endpoints=[
                {"port_id":"urn:sdx:port:test:1", "vlan": "100"}
            ]

        self.assertEqual(str(context.exception), "Endpoints must contain at least 2 entries.")

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_endpoints_type_check(self, mock_post):
        """Checks that the 'endpoints' setter raises 'TypeError' when 'endpoints' is not a list."""
        client = SDXClient(base_url="http://example.com")
        client.name="Test L2VPN"


        with self.assertRaises(TypeError) as context:
            client.endpoints = "invalid endpoints"

        self.assertEqual(str(context.exception), "Endpoints must be a list.")

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_endpoints_list_of_dicts_check(self, mock_post):
        """Checks that the 'endpoints' setter raises 'TypeError' when 'endpoints' contains non-dictionary elements."""
        client = SDXClient(base_url="http://example.com")
        client.name="Test L2VPN"

        with self.assertRaises(TypeError) as context:
            client.endpoints=[
                {"port_id":"urn:sdx:port:test:1", "vlan": "100"},
                "invalid endpoint"
            ]

        self.assertEqual(str(context.exception), "Endpoints must be a list of dictionaries.")

    #### API Call Fails ####
    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_failure(self, mock_post):
        """Checks that the 'create_l2vpn' method correctly handles a failure scenario where the API call returns an error response."""
        mock_post.return_value.ok = False
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = "Bad Request"

        client = SDXClient(base_url="http://example.com")
        client.name="Test L2VPN"
        client.endpoints=[
                {"port_id": "urn:sdx:port:test:1", "vlan": "100"},
                {"port_id": "urn:sdx:port:test:1", "vlan": "200"}
        ]

        with self.assertRaises(SDXException) as context:
            client.create_l2vpn()

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.message, "Bad Request")

if __name__=="__main__":
    unittest.main()