import unittest
from unittest.mock import patch
from sdxlib.client import SDXClient, SDXException


"""
Unit tests for the sdxlib library

Run from the SDXLIB parent directory Using:
    python -m unittest discover -v tests
"""


class TestSDXClient(unittest.TestCase):

    # API Call Succeeds
    @patch("sdxlib.client.requests.post")
    def test_create_l2vpn_success(self, mock_post):
        """Checks that the 'create_l2vpn' method correctly handles a
        successful API call."""
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {"status": "Accepted"}

        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]

        response = client.create_l2vpn()

        self.assertEqual(response, {"status": "Accepted"})

        mock_post.assert_called_once_with(
            "http://example.com/l2vpn",
            json={
                "name": "Test L2VPN",
                "endpoints": [
                    {
                        "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                        "vlan": "100",
                    },
                    {
                        "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                        "vlan": "200",
                    },
                ],
            },
        )

    # API Call Fails
    @patch("sdxlib.client.requests.post")
    def test_create_l2vpn_api_failure(self, mock_post):
        """Checks that the 'create_l2vpn' method raises an
        'SDXException on API failure."""
        mock_post.return_value.ok = False
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Internal Server Error"

        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]

        with self.assertRaises(SDXException) as context:
            client.create_l2vpn()

        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(context.exception.message, "Internal Server Error")
        mock_post.assert_called_once()

    # Unit Tests for Name Attribute#
    def test_create_l2vpn_name_required(self):
        """Checks that 'name' is provided."""
        client = SDXClient(base_url="http://example.com")
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]
        with self.assertRaises(ValueError) as context:
            client.create_l2vpn()
        self.assertEqual(str(context.exception), "Name attribute is required.")

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
            client.name = "This is a very long name that exceeds 50 chatacters limit"
        self.assertEqual(str(context.exception), "Name must be 50 characters or fewer.")

    def test_name_non_string(self):
        """Checks that a non-string value is not allowed for the 'name' attribute."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(TypeError) as context:
            client.name = 123
        self.assertEqual(str(context.exception), "Name must be a string.")

    # Unit Tests for Endpoints Attribute#
    def test_create_l2vpn_endpoints_required(self):
        """Checks that 'endpoints' is provided."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        with self.assertRaises(ValueError) as context:
            client.create_l2vpn()
        self.assertEqual(str(context.exception), "Endpoints attribute is required.")

    def test_endpoints_list_check(self):
        """Checks that non-list value is not allowed for the 'endpoints' attribute."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        with self.assertRaises(TypeError) as context:
            client.endpoints = "invalid endpoints"
        self.assertEqual(str(context.exception), "Endpoints must be a list.")

    def test_endpoints_empty_list(self):
        """Checks that an empty list is not allowed for the 'endpoints' attribute."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = []
        self.assertEqual(
            str(context.exception), "Endpoints must contain at least 2 entries."
        )

    def test_endpoints_min_required(self):
        """Checks that a list with less than 2 endpoints is not allowed."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "100",
                }
            ]
        self.assertEqual(
            str(context.exception), "Endpoints must contain at least 2 entries."
        )

    def test_endpoints_list_of_dicts_check(self):
        """Checks that a list of non-dictionary elements is not allowed in the 'endpoints' attribute."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        with self.assertRaises(TypeError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "100",
                },
                "invalid endpoint",
            ]
        self.assertEqual(
            str(context.exception), "Endpoints must be a list of dictionaries."
        )

    # Unit Tests for Endpoints[Port ID] Attribute #
    def test_endpoints_missing_port_id(self):
        """Checks that each endpoint contains a 'port_id' key."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "100",
                },
                {"vlan": "200"},
            ]
        self.assertEqual(
            str(context.exception),
            "Each endpoint must contain a non-empty 'port_id' key.",
        )

    def test_endpoints_empty_port_id(self):
        """Checks that each endpoint's 'port_id' key cannot be empty."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {"port_id": "", "vlan": "100"},
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "Each endpoint must contain a non-empty 'port_id' key.",
        )

    def test_endpoints_invalid_port_id_format(self):
        """Checks that the 'port_id' key follows the required format."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {"port_id": "invalid-port_id", "vlan": "100"},
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200",
                },
            ]
        self.assertEqual(
            str(context.exception), "Invalid port_id format: invalid-port_id"
        )

    # Unit Tests for Endpoints[VLAN] Attribute #
    def test_endpoints_missing_vlan_key(self):
        """Checks that each endpoint contains a 'vlan' key."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "100",
                },
                {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2"},
            ]
        self.assertEqual(
            str(context.exception), "Each endpoint must contain a non-empty 'vlan' key."
        )

    def test_endpoints_empty_vlan_value(self):
        """Checks that each endpoint's 'vlan' key cannot be empty."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200",
                },
            ]
        self.assertEqual(
            str(context.exception), "Each endpoint must contain a non-empty 'vlan' key."
        )

    # VLAN Integer String #
    def test_endpoints_vlan_integer_string_valid(self):
        """Checks that setting a VLAN ID as a valid integer string works."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]
        self.assertEqual(
            client.endpoints,
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "100",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200",
                },
            ],
        )

    def test_endpoints_vlan_integer_not_string(self):
        """Checks that setting a 'vlan' as an integer raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(TypeError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": 100,
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200",
                },
            ]
        self.assertEqual(str(context.exception), "VLAN must be a string.")

    # VLAN value "any" #
    def test_endpoints_vlan_any_single(self):
        """Checks that setting a VLAN to 'any' for a single endpoint works."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "any",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]
        self.assertEqual(
            client.endpoints,
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "any",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200",
                },
            ],
        )

    def test_endpoints_vlan_any_untagged(self):
        """Checks that setting VLANs to 'any' and 'untagged' works together."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "any",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "untagged",
            },
        ]
        self.assertEqual(
            client.endpoints,
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "any",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "untagged",
                },
            ],
        )

    def test_endpoints_vlan_any_multiple(self):
        """Checks that setting VLAN to 'any' for multiple endpoints works."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "any",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "any",
            },
        ]
        self.assertEqual(
            client.endpoints,
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "any",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "any",
                },
            ],
        )

    def test_endpoints_vlan_any_mixed(self):
        """Checks that setting VLAN to 'any' with other specific VLAN IDs works."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "any",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name3",
                "vlan": "any",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name4",
                "vlan": "300",
            },
        ]
        self.assertEqual(
            client.endpoints,
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "any",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name3",
                    "vlan": "any",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name4",
                    "vlan": "300",
                },
            ],
        )

    def test_endpoints_vlan_any_invalid_value(self):
        """Checks that setting an invalid VLAN raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "any",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "5000",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "Invalid VLAN value: '5000'. Must be 'any', 'all', 'untagged', a string representing an integer between 1 and 4095, or a range.",
        )

    # VLAN value "untagged" #
    def test_endpoints_vlan_untagged_single(self):
        """Checks that setting a VLAN to 'untagged' for a single endpoint works."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "untagged",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]
        self.assertEqual(
            client.endpoints,
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "untagged",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200",
                },
            ],
        )

    def test_endpoints_vlan_untagged_multiple(self):
        """Checks that setting VLAN to 'untagged' for multiple endpoints works."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "untagged",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "untagged",
            },
        ]
        self.assertEqual(
            client.endpoints,
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "untagged",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "untagged",
                },
            ],
        )

    def test_endpoints_vlan_untagged_mixed(self):
        """Checks that setting VLAN to 'untagged' with other specific VLAN IDs works."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "untagged",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name3",
                "vlan": "untagged",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name4",
                "vlan": "300",
            },
        ]
        self.assertEqual(
            client.endpoints,
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "untagged",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name3",
                    "vlan": "untagged",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name4",
                    "vlan": "300",
                },
            ],
        )

    def test_endpoints_vlan_invalid_value(self):
        """Checks that setting an invalid VLAN raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "untagged",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "5000",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "Invalid VLAN value: '5000'. Must be 'any', 'all', 'untagged', a string representing an integer between 1 and 4095, or a range.",
        )

    # VLAN range #
    def test_endpoints_vlan_range_valid(self):
        """Checks that setting a valid VLAN range works."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "100:200",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "100:200",
            },
        ]
        self.assertEqual(
            client.endpoints,
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "100:200",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "100:200",
                },
            ],
        )

    def test_endpoints_vlan_range_empty_vlan_value(self):
        """Checks that each endpoint's 'vlan' key cannot be empty when used with range."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "100:200",
                },
            ]
        self.assertEqual(
            str(context.exception), "Each endpoint must contain a non-empty 'vlan' key."
        )

    def test_endpoints_vlan_range_mismatch(self):
        """Checks that setting a VLAN range for one endpoint and a different range for another raised a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "100:200",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200:300",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "All endpoints must have the same VLAN value if one endpoint is 'all' or a range.",
        )

    def test_endpoints_vlan_range_single_endpoint(self):
        """Checks that setting a VLAN range for one endpoint and a single VLAN for another raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "100:200",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "300",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "All endpoints must have the same VLAN value if one endpoint is 'all' or a range.",
        )

    def test_endpoints_vlan_range_invalid_endpoint(self):
        """Checks that setting a VLAN range for one endpoint and an invlaid value for another raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "100:200",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "invalid value",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "Invalid VLAN value: 'invalid value'. Must be 'any', 'all', 'untagged', a string representing an integer between 1 and 4095, or a range.",
        )

    def test_endpoints_vlan_range_and_any(self):
        """Checks that setting a VLAN range and 'any' raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "100:200",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "any",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "All endpoints must have the same VLAN value if one endpoint is 'all' or a range.",
        )

    def test_endpoints_vlan_range_and_untagged(self):
        """Checks that setting a VLAN range and 'untagged' raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "100:200",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "untagged",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "All endpoints must have the same VLAN value if one endpoint is 'all' or a range.",
        )

    def test_endpoints_vlan_range_and_all(self):
        """Checks that setting a VLAN range and 'all' raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "100:200",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "all",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "All endpoints must have the same VLAN value if one endpoint is 'all' or a range.",
        )

    def test_endpoints_vlan_range_invalid_format(self):
        """Checks that setting an invalid VLAN range raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200:100",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200:100",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "Invalid VLAN range values: '200:100'. Must be between 1 and 4095, and VLAN ID1 must be less than VLAN ID2.",
        )

    def test_endpoints_vlan_range_out_of_bounds_0(self):
        """Checks that setting a VLAN range out of the lower bound raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "0:200",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "0:200",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "Invalid VLAN range values: '0:200'. Must be between 1 and 4095, and VLAN ID1 must be less than VLAN ID2.",
        )

    def test_endpoints_vlan_range_out_of_bounds_4096(self):
        """Checks that setting a VLAN range out of the upper bould raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "4000:4096",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "4000:4096",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "Invalid VLAN range values: '4000:4096'. Must be between 1 and 4095, and VLAN ID1 must be less than VLAN ID2.",
        )

    def test_endpoints_vlan_range_and_invalid_vlan(self):
        """Checks that setting a VLAN range and an invalid VLAN value raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "100:200",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "5000",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "Invalid VLAN value: '5000'. Must be 'any', 'all', 'untagged', a string representing an integer between 1 and 4095, or a range.",
        )

    # VLAN value "all" #
    def test_endpoints_vlan_all_valid(self):
        """Checks that setting a VLAN to 'all' for a single endpoint works if all endpoints have 'all'."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name",
                "vlan": "all",
            },
            {
                "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name2",
                "vlan": "all",
            },
        ]
        self.assertEqual(
            client.endpoints,
            [
                {
                    "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name",
                    "vlan": "all",
                },
                {
                    "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name2",
                    "vlan": "all",
                },
            ],
        )

    def test_endpoints_vlan_intger(self):
        """Checks that setting a VLAN to 'all' with other VLAN values raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name",
                    "vlan": "all",
                },
                {
                    "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name2",
                    "vlan": "100",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "All endpoints must have the same VLAN value if one endpoint is 'all' or a range.",
        )

    def test_endpoints_vlan_all_any(self):
        """Checks that setting a VLAN to 'all' with 'any' raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name",
                    "vlan": "all",
                },
                {
                    "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name2",
                    "vlan": "any",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "All endpoints must have the same VLAN value if one endpoint is 'all' or a range.",
        )

    def test_endpoints_vlan_all_untagged(self):
        """Checks that setting a VLAN to 'all' with 'untagged' raises a ValueError."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name",
                    "vlan": "all",
                },
                {
                    "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name2",
                    "vlan": "untagged",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "All endpoints must have the same VLAN value if one endpoint is 'all' or a range.",
        )

    # Other VLAN value tests #
    def test_endpoints_valid_vlan_format(self):
        """Checks that the 'vlan' key follows the required format."""
        client = SDXClient(base_url="http://example.com")
        with self.assertRaises(ValueError) as context:
            client.endpoints = [
                {
                    "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name",
                    "vlan": "100",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "invalid_vlan",
                },
            ]
        self.assertEqual(
            str(context.exception),
            "Invalid VLAN value: 'invalid_vlan'. Must be 'any', 'all', 'untagged', a string representing an integer between 1 and 4095, or a range.",
        )

    # Unit Tests for Description Attribute(Optional) #
    def test_set_valid_description(self):
        """Test setting a valid 'description' value of string."""
        client = SDXClient(base_url="http://example.com")
        valid_description = "This is a valid description."
        client.description = valid_description
        self.assertEqual(client.description, valid_description)

    def test_set_valid_description_url(self):
        """Test setting a valid 'description' value of URL."""
        client = SDXClient(base_url="http://example.com")
        valid_description = "https://example.com/info"
        client.description = valid_description
        self.assertEqual(client.description, valid_description)

    def test_set_description_none(self):
        """Test setting the description to None."""
        client = SDXClient(base_url="http://example.com")
        client.description = None
        self.assertIsNone(client.description)

    def test_set_description_exceeding_limit(self):
        """Test setting description exceeding 255-character limit will raise ValueError"""
        client = SDXClient(base_url="http://example.com")
        long_description = "x" * 256
        with self.assertRaises(ValueError) as context:
            client.description = long_description
        self.assertEqual(
            str(context.exception),
            "Description attribute must be less than 256 characters.",
        )

    # Unit Tests for Notifications Attribute(Optional) #

    def test_notifications_valid(self):
        """Test setting and getting valid notifications within the 10-email limit."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]
        valid_notifications = [
            {
                "email":
                "user1@email.com",
            },
            {
                "email":
                "user2@email.com",
            },
        ]
        client.notifications = valid_notifications
        self.assertEqual(
            client.notifications,
            valid_notifications
        )


    def test_notifications_not_list(self):
        """Test setting notifications with a non-list value, expecting a ValueError."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]
        invalid_notifications = {
            "email":
            "user1@email.com",
        },
        with self.assertRaises(ValueError) as context:
            client.notifications = invalid_notifications
        self.assertEqual(
            str(context.exception),
            "Notifications must be provided as a list."
        )

    def test_notifications_list_element_not_dict(self):
        """Test setting notifications with a non-dictionary entry, expecting a ValueError."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]
        invalid_notifications = [
            {
                "email":
                "user1@email.com",
            },
            "not a dict"
        ]
        with self.assertRaises(ValueError) as context:
            client.notifications = invalid_notifications
        self.assertEqual(
            str(context.exception),
            "Each notification must be a dictionary with an 'email' key."
        )


    def test_notifications_dict_no_email_key(self):
        """Test setting notification with a dictionary missing the 'email' key, expecting a ValueError."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]
        invalid_notifications = [
            {
                "email":
                "user1@email.com",
            },
            {
                "not_email":
                "user2@email.com",
            },
        ]
        with self.assertRaises(ValueError) as context:
            client.notifications = invalid_notifications
        self.assertEqual(
            str(context.exception),
            "Each notification must be a dictionary with an 'email' key."
        )

    def test_notifications_dict_non_valid_email(self):
        """Test setting notifications with an invalid email format, expecting a ValueError."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]
        invalid_notifications = [
            {
                "email":
                "user1@email.com",
            },
            {
                "email":
                "invalid_email",
            },
        ]
        with self.assertRaises(ValueError) as context:
            client.notifications = invalid_notifications
        self.assertEqual(
            str(context.exception),
            "Each 'email' value must be a valid email address."
        )

    def test_notifications_list_too_long(self):
        """Test setting notifications exceeding 10-email limit, expecting a ValueError."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        client.endpoints = [
            {
                "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]
        exceeding_notifications = [
            {
                "email": f"user{i}@email.com" 
            } for i in range(11)
        ]
        with self.assertRaises(ValueError) as context:
            client.notifications = exceeding_notifications
        self.assertEqual(
            str(context.exception),
            "Notifications can contain at most 10 email addresses."
        )

    # Additional Success Tests #
    def test_valid_name(self):
        """Checks that a valid name is accepted."""
        client = SDXClient(base_url="http://example.com")
        client.name = "Test L2VPN"
        self.assertEqual(client.name, "Test L2VPN")

    def test_valid_endpoints(self):
        """Checks that valid endpoints are accepted."""
        client = SDXClient(base_url="http://example.com")
        valid_endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "200",
            },
        ]
        client.endpoints = valid_endpoints
        self.assertEqual(client.endpoints, valid_endpoints)


if __name__ == "__main__":
    unittest.main()
