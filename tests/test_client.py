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
    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_success(self, mock_post):
        """Checks that the 'create_l2vpn' method correctly handles a successful API call."""
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {"status": "Accepted"}

        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints=[
            {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan": "100"},
            {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2", "vlan": "200"}
        ]
        
        response = client.create_l2vpn()

        self.assertEqual(response, {"status": "Accepted"})
        mock_post.assert_called_once_with(
            "http://example.com/l2vpn",
            json={
                "name": "Test L2VPN",
                "endpoints": [
                    {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan": "100"},
                    {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2", "vlan": "200"}
                ]
            }
        )

    #### API Call Fails ####
    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_api_failure(self, mock_post):
        """Checks that the 'create_l2vpn' method raises and 'SDXException on API failure."""
        mock_post.return_value.ok = False
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Internal Server Error"

        client = SDXClient(base_url="http://example.com")
        client.name="Test L2VPN"
        client.endpoints=[
                {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan": "100"},
                {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2", "vlan": "200"}
        ]

        with self.assertRaises(SDXException) as context:
            client.create_l2vpn()

        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(context.exception.message, "Internal Server Error")
        mock_post.assert_called_once()

    #### Edge Cases for Name ####
    def test_name_not_set(self):
        """Checks that 'name' is provided."""
        client = SDXClient(base_url="http://example.com")
        client.endpoints=[
            {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan": "100"},
            {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2", "vlan": "200"}
        ]
        with self.assertRaises(ValueError) as context:
            client.create_l2vpn()
        self.assertEqual(str(context.exception), "Name is required.")

    def test_name_empty_string(self):
        """Checks that empty string is not allowed for 'name' attribute."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.name = ""
        self.assertEqual(str(context.exception), "Name cannot be an empty string.")

    def test_name_too_long(self):
        """Checks that the 'name' exceeding 50 characters is not allowed."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.name="This is a very long name that exceeds 50 chatacters limit"
        self.assertEqual(str(context.exception), "Name must be 50 characters or fewer.")

    def test_name_non_string(self):
        """Checks that a non-string value is not allowed for the 'name' attribute."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(TypeError) as context:
            client.name = 123
        self.assertEqual(str(context.exception), "Name must be a string.")

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
                {"port_id":"urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan": "100"}
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
                {"port_id":"urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan": "100"},
                "invalid endpoint"
            ]

        self.assertEqual(str(context.exception), "Endpoints must be a list of dictionaries.")

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_endpoints_invalid_port_id(self, mock_post):
        """Checks that the 'endpoints' setter raises 'ValueError' when 'port_id' has an invalid format."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"

        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {"port_id": "invalid-port_id", "vlan": "100"},
                {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2", "vlan":"200"}
            ]

        self.assertEqual(str(context.exception), "Invalid port_id format: invalid-port_id")

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_endpoints_missing_port_id(self, mock_post):
        """Checks that the 'endpoints'setter raises 'ValueError' when any endpoint is missing the 'port_id' key. """
        
        client = SDXClient(base_url="http://example.com")
        client.name="Test L2VPN"

        with self.assertRaises(ValueError) as context:
            client.endpoints=[
                {"port_id":"urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan":"100"},
                {"vlan":"200"}
            ]

        self.assertEqual(str(context.exception), "Each endpoint must contain a non-empty 'port_id' key.")

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_endpoints_missing_vlan(self, mock_post):
        """Checks that the 'endpoints'setter raises 'ValueError' when any endpoint is missing the 'vlan' key. """

        client = SDXClient(base_url="http://example.com")
        client.name="Test L2VPN"

        with self.assertRaises(ValueError) as context:
            client.endpoints=[
                {"port_id":"urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan":"100"},
                {"port_id":"urn:sdx:port:test-oxp_url:test-node_name:test-port_name2"}
            ]

        self.assertEqual(str(context.exception), "Each endpoint must contain a non-empty 'vlan' key.")

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_endpoints_empty_port_id(self, mock_post):
        """Checks that the 'endpoints' setter raises 'ValueError' when any 'port_id' key has a missing value."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"

        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {"port_id": "", "vlan": "100"}, 
                {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2", "vlan": "200"}
            ]

        self.assertEqual(str(context.exception), "Each endpoint must contain a non-empty 'port_id' key.")

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_endpoints_empty_vlan(self, mock_post):
        """Checks that the 'endpoints' setter raises 'ValueError' when any 'vlan' key has a missing value."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"

        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan": ""},
                {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2", "vlan": "200"}
            ]

        self.assertEqual(str(context.exception), "Each endpoint must contain a non-empty 'vlan' key.")

if __name__=="__main__":
    unittest.main()