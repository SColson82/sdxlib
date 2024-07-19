import requests
import unittest
from unittest.mock import patch
from sdxlib.sdx_client import SDXClient, SDXException

class TestSDXClient(unittest.TestCase):
    # Unit Tests for Description Attribute(Optional) #
    def test_set_valid_description(self):
        """Test setting a valid 'description' value of string."""
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
            base_url="http://example.com", name=client_name, endpoints=client_endpoints
        )
        valid_description = "This is a valid description."
        client.description = valid_description
        self.assertEqual(client.description, valid_description)

    def test_set_valid_description_url(self):
        """Test setting a valid 'description' value of URL."""
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
            base_url="http://example.com", name=client_name, endpoints=client_endpoints
        )
        valid_description = "https://example.com/info"
        client.description = valid_description
        self.assertEqual(client.description, valid_description)

    def test_set_description_none(self):
        """Test setting the description to None."""
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
            base_url="http://example.com", name=client_name, endpoints=client_endpoints
        )
        client.description = None
        self.assertIsNone(client.description)

    def test_set_description_exceeding_limit(self):
        """Test setting description exceeding 255-character limit will raise ValueError"""
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
            base_url="http://example.com", name=client_name, endpoints=client_endpoints
        )
        long_description = "x" * 256
        with self.assertRaises(ValueError) as context:
            client.description = long_description
        self.assertEqual(
            str(context.exception),
            "Description attribute must be less than 256 characters.",
        )


# Run the tests
if __name__ == "__main__":
    unittest.main()