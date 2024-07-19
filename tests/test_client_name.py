import requests
import unittest
from unittest.mock import patch
from sdxlib.sdx_client import SDXClient, SDXException

class TestSDXClient(unittest.TestCase):

    def test_name_empty_string(self):
        """Checks that empty string is not allowed for 'name' attribute."""
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
        with self.assertRaises(ValueError) as context:
            client.name = ""
        self.assertEqual(
            str(context.exception),
            "Name must be a non-empty string with maximum 50 characters.",
        )

    def test_name_too_long(self):
        """Checks that the 'name' exceeding 50 characters is not allowed."""
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
        with self.assertRaises(ValueError) as context:
            client.name = "This is a very long name that exceeds 50 chatacters limit"
        self.assertEqual(
            str(context.exception),
            "Name must be a non-empty string with maximum 50 characters.",
        )

    def test_name_non_string(self):
        """Checks that a non-string value is not allowed for the 'name' attribute."""
        client_url = "http://example.com"
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
        client = SDXClient(base_url=client_url, endpoints=client_endpoints)
        with self.assertRaises(ValueError) as context:
            client.name = 123
        self.assertEqual(str(context.exception), "Name must be a non-empty string with maximum 50 characters.")

    def test_valid_name(self):
        """Checks that a valid name is accepted."""
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
        self.assertEqual(client.name, "Test L2VPN")


# Run the tests
if __name__ == "__main__":
    unittest.main()