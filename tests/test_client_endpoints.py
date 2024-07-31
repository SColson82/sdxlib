import unittest
from sdxlib.sdx_client import SDXClient
from test_config import TEST_URL, TEST_NAME, TEST_ENDPOINTS


class TestSDXClient(unittest.TestCase):
    def test_endpoints_list_check(self):
        """Checks that non-list value is not allowed for the 'endpoints' attribute."""
        with self.assertRaises(TypeError) as context:
            SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints="invalid endpoints")
        self.assertEqual(str(context.exception), "Endpoints must be a list.")

    def test_endpoints_empty_list(self):
        """Checks that an empty list is not allowed for the 'endpoints' attribute."""
        with self.assertRaises(ValueError) as context:
            SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=[])
        self.assertEqual(
            str(context.exception), "Endpoints must contain at least 2 entries."
        )

    def test_endpoints_min_required(self):
        """Checks that a list with less than 2 endpoints is not allowed."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
            "Invalid VLAN value: '5000'. Must be between 1 and 4095.",
        )

    # VLAN value "untagged" #
    def test_endpoints_vlan_untagged_single(self):
        """Checks that setting a VLAN to 'untagged' for a single endpoint works."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
            "Invalid VLAN value: '5000'. Must be between 1 and 4095.",
        )

    # VLAN range #
    def test_endpoints_vlan_range_valid(self):
        """Checks that setting a valid VLAN range works."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
            "Invalid VLAN range format: '200:100'. Must be 'VLAN ID1:VLAN ID2'.",
        )

    def test_endpoints_vlan_range_out_of_bounds_0(self):
        """Checks that setting a VLAN range out of the lower bound raises a ValueError."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
            "Invalid VLAN range format: '0:200'. Must be 'VLAN ID1:VLAN ID2'.",
        )

    def test_endpoints_vlan_range_out_of_bounds_4096(self):
        """Checks that setting a VLAN range out of the upper bould raises a ValueError."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
            "Invalid VLAN range format: '4000:4096'. Must be 'VLAN ID1:VLAN ID2'.",
        )

    def test_endpoints_vlan_range_and_invalid_vlan(self):
        """Checks that setting a VLAN range and an invalid VLAN value raises a ValueError."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
            "Invalid VLAN value: '5000'. Must be between 1 and 4095.",
        )

    # VLAN value "all" #
    def test_endpoints_vlan_all_valid(self):
        """Checks that setting a VLAN to 'all' for a single endpoint works if all endpoints have 'all'."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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

    def test_valid_endpoints(self):
        """Checks that valid endpoints are accepted."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
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
        # client.endpoints = valid_endpoints
        self.assertEqual(client.endpoints, valid_endpoints)


# Run the tests
if __name__ == "__main__":
    unittest.main()
