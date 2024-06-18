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

    #### Edge Case Tests for Name ####
    def test_create_l2vpn_name_required(self):
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

    #### Edge Case Tests for Endpoints ####
    def test_create_l2vpn_endpoints_required(self):
        """Checks that the 'create_l2vpn' method correctly raises a 'ValueError' when the endpoints list is empty."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        with self.assertRaises(ValueError) as context:
            client.create_l2vpn()
        self.assertEqual(str(context.exception), "Endpoints must not be empty.")

    def test_endpoints_empty_list(self):
        """Checks that an empty list is not allowed for the 'endpoints' attribute."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = []
        self.assertEqual(str(context.exception), "Endpoints must contain at least 2 entries.")

    def test_endpoints_min_required(self):
        """Checks that a list with less than 2 endpoints is not allowed."""
        client = SDXClient(base_url="http://example.com")
        client.name="Test L2VPN"
        with self.assertRaises(ValueError) as context:
            client.endpoints=[
                {"port_id":"urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan": "100"}
            ]
        self.assertEqual(str(context.exception), "Endpoints must contain at least 2 entries.")

    def test_endpoints_list_check(self):
        """Checks that non-list value is not allowed for the 'endpoints' attribute."""
        client = SDXClient(base_url="http://example.com")
        client.name="Test L2VPN"
        with self.assertRaises(TypeError) as context:
            client.endpoints = "invalid endpoints"
        self.assertEqual(str(context.exception), "Endpoints must be a list.")

    def test_endpoints_list_of_dicts_check(self):
        """Checks that a list of non-dictionary elements is not allowed in the 'endpoints' attribute."""
        client = SDXClient(base_url="http://example.com")
        client.name="Test L2VPN"
        with self.assertRaises(TypeError) as context:
            client.endpoints=[
                {"port_id":"urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan": "100"},
                "invalid endpoint"
            ]
        self.assertEqual(str(context.exception), "Endpoints must be a list of dictionaries.")

    ### Edge Case Tests for Endpoints['port_id'] ###
    def test_endpoints_missing_port_id(self):
        """Checks that each endpoint contains a 'port_id' key. """
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints=[
                {"port_id":"urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan":"100"},
                {"vlan":"200"}
            ]
        self.assertEqual(str(context.exception), "Each endpoint must contain a non-empty 'port_id' key.")

    def test_endpoints_empty_port_id(self):
        """Checks that each endpoint's 'port_id' key cannot be empty."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {"port_id": "", "vlan": "100"}, 
                {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2", "vlan": "200"}
            ]
        self.assertEqual(str(context.exception), "Each endpoint must contain a non-empty 'port_id' key.")

    def test_endpoints_invalid_port_id_format(self):
        """Checks that the 'port_id' key follows the required format."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {"port_id": "invalid-port_id", "vlan": "100"},
                {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2", "vlan":"200"}
            ]
        self.assertEqual(str(context.exception), "Invalid port_id format: invalid-port_id")

    def test_endpoints_missing_vlan(self):
        """Checks that each endpoint contains a 'vlan' key."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints=[
                {"port_id":"urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan":"100"},
                {"port_id":"urn:sdx:port:test-oxp_url:test-node_name:test-port_name2"}
            ]
        self.assertEqual(str(context.exception), "Each endpoint must contain a non-empty 'vlan' key.")

    def test_endpoints_empty_vlan(self):
        """Checks that each endpoint's 'vlan' key cannot be empty."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name", "vlan": ""},
                {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2", "vlan": "200"}
            ]
        self.assertEqual(str(context.exception), "Each endpoint must contain a non-empty 'vlan' key.")

if __name__=="__main__":
    unittest.main()