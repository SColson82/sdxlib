import requests
import unittest
from unittest.mock import patch
from sdxlib.sdx_client import SDXClient, SDXException

class TestSDXClient(unittest.TestCase):
    # # API Call Succeeds
    @patch("requests.post")  # Mock the requests.post function
    def test_create_l2vpn_success(self, mock_post):
        # Set up mock response
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {"service_id": "123"}
        mock_post.return_value = mock_response

        # Create SDXClient object with sample data
        client_name = "Test L2VPN"
        client_endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]

        client = SDXClient(
            base_url="https:/api.example.com",
            name=client_name,
            endpoints=client_endpoints,
            description="Test Description",
        )
        # Call the function and assert the response
        response = client.create_l2vpn()

        self.assertEqual(response, {"service_id": "123"})
    
        # Verify that requests.post was called with expected URL and payload parts
        mock_post.assert_called_once_with(
            "https:/api.example.com/l2vpn/1.0",
            json={
                "name": client_name,
                "endpoints": client_endpoints,
                "description": "Test Description",
            },
            timeout=120,
        )

    @patch("requests.post")
    def test_create_l2vpn_error(self, mock_post):
        # Set up mock error
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        # Create SDXClient object
        url = "https:/api.example.com"
        client_name = "Test L2VPN"
        client_endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]

        client = SDXClient(
            base_url=url,
            name=client_name,
            endpoints=client_endpoints,
        )

        # Call the function and assert it raises SDXException
        with self.assertRaises(SDXException) as context:
            client.create_l2vpn()
        self.assertEqual(str(context.exception), "An error occurred while creating L2VPN: Connection error")

        # Verify that requests.post was called
        mock_post.assert_called_once()

    def test_create_l2vpn_url_required(self):
        """Checks that 'base_url' is provided."""
        client_name = "Test L2VPN"
        client_endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]

        client = SDXClient(
            name=client_name,
            endpoints=client_endpoints,
        )
        with self.assertRaises(ValueError) as context:
            client.create_l2vpn()
        self.assertEqual(str(context.exception), "Creating L2VPN requires the base URL, name, and endpoints at minumum.")

    def test_create_l2vpn_name_required(self):
        """Checks that 'name' is provided."""
        url = "http://example.com"
        client_endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]

        client = SDXClient(
            base_url=url,
            endpoints=client_endpoints,
        )
        with self.assertRaises(ValueError) as context:
            client.create_l2vpn()
        self.assertEqual(str(context.exception), "Creating L2VPN requires the base URL, name, and endpoints at minumum.")

    def test_create_l2vpn_endpoints_required(self):
        """Checks that 'endpoints' is provided."""
        url = "http://example.com"
        client_name = "Test L2VPN"
        with self.assertRaises(TypeError) as context:
            client = SDXClient(
                base_url=url,
                name=client_name,
            )
            client.create_l2vpn()
        self.assertEqual(str(context.exception), "Endpoints must be a list.")

# Run the tests
if __name__ == "__main__":
    unittest.main()