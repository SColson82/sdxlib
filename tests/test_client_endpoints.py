import unittest
from sdxlib.sdx_client import SDXClient
from test_config import (
    create_client,
    VLAN_100,
    VLAN_200,
    VLAN_ALL,
    VLAN_ANY,
    VLAN_RANGE,
    VLAN_UNTAGGED,
    ERROR_INVALID_ENDPOINTS,
    ERROR_EMPTY_ENDPOINTS_LIST,
    ERROR_MIN_ENTRIES,
    ERROR_LIST_OF_DICTS,
    ERROR_NONEMPTY_PORT_ID,
    ERROR_INVALID_PORT_ID_FORMAT,
    ERROR_EMPTY_VLAN_VALUE,
    ERROR_INVALID_VLAN_TYPE,
    ERROR_INVALID_VLAN_VALUE,
    ERROR_VLAN_RANGE_MISMATCH,
    ERROR_VLAN_INVALID,
    ERROR_VLAN_RANGE_VALUE,
)


class TestSDXClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client = create_client()

    def assert_invalid_endpoints(
        self, invalid_value, expected_message, exception=ValueError
    ):
        with self.assertRaises(exception) as context:
            self.client.endpoints = invalid_value
        self.assertEqual(str(context.exception), expected_message)

    def test_endpoints_list_check(self):
        """Checks that non-list value is not allowed for the 'endpoints' attribute."""
        self.assert_invalid_endpoints(
            "invalid endpoints", ERROR_INVALID_ENDPOINTS, TypeError
        )

    def test_endpoints_empty_list(self):
        """Checks that an empty list is not allowed for the 'endpoints' attribute."""
        self.assert_invalid_endpoints([], ERROR_EMPTY_ENDPOINTS_LIST)

    def test_endpoints_min_required(self):
        """Checks that a list with less than 2 endpoints is not allowed."""
        self.assert_invalid_endpoints([VLAN_100,], ERROR_MIN_ENTRIES)

    def test_endpoints_list_of_dicts_check(self):
        """Checks that a list of non-dictionary elements is not allowed in the 'endpoints' attribute."""
        self.assert_invalid_endpoints(
            [VLAN_100, "invalid endpoint"], ERROR_LIST_OF_DICTS, TypeError
        )

    # Unit Tests for Endpoints[Port ID] Attribute #
    def test_endpoints_missing_port_id(self):
        """Checks that each endpoint contains a 'port_id' key."""
        self.assert_invalid_endpoints(
            [VLAN_100, {"vlan": "200"}], ERROR_NONEMPTY_PORT_ID
        )

    def test_endpoints_empty_port_id(self):
        """Checks that each endpoint's 'port_id' key cannot be empty."""
        self.assert_invalid_endpoints(
            [{"port_id": "", "vlan": "100"}, VLAN_200], ERROR_NONEMPTY_PORT_ID
        )

    def test_endpoints_invalid_port_id_format(self):
        """Checks that the 'port_id' key follows the required format."""
        self.assert_invalid_endpoints(
            [{"port_id": "invalid-port_id", "vlan": "100"}, VLAN_200],
            ERROR_INVALID_PORT_ID_FORMAT,
        )

    # Unit Tests for Endpoints[VLAN] Attribute #
    def test_endpoints_missing_vlan_key(self):
        """Checks that each endpoint contains a 'vlan' key."""
        self.assert_invalid_endpoints(
            [
                VLAN_100,
                {"port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2"},
            ],
            ERROR_EMPTY_VLAN_VALUE,
        )

    def test_endpoints_empty_vlan_value(self):
        """Checks that each endpoint's 'vlan' key cannot be empty."""
        self.assert_invalid_endpoints(
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": "",
                },
                VLAN_200,
            ],
            ERROR_EMPTY_VLAN_VALUE,
        )

    # VLAN Integer String #
    def test_endpoints_vlan_integer_string_valid(self):
        """Checks that setting a VLAN ID as a valid integer string works."""
        self.assertEqual(self.client.endpoints, [VLAN_100, VLAN_200])

    def test_endpoints_vlan_integer_not_string(self):
        """Checks that setting a 'vlan' as an integer raises a ValueError."""
        self.assert_invalid_endpoints(
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                    "vlan": 100,
                },
                VLAN_200,
            ],
            ERROR_INVALID_VLAN_TYPE,
            TypeError,
        )

    # VLAN value "any" #
    def test_endpoints_vlan_any_single(self):
        """Checks that setting a VLAN to 'any' for a single endpoint works."""
        self.client.endpoints = [VLAN_ANY, VLAN_200]
        self.assertEqual(self.client.endpoints, [VLAN_ANY, VLAN_200])

    def test_endpoints_vlan_any_untagged(self):
        """Checks that setting VLANs to 'any' and 'untagged' works together."""
        self.client.endpoints = [VLAN_ANY, VLAN_UNTAGGED]
        self.assertEqual(self.client.endpoints, [VLAN_ANY, VLAN_UNTAGGED])

    def test_endpoints_vlan_any_multiple(self):
        """Checks that setting VLAN to 'any' for multiple endpoints works."""
        self.client.endpoints = [
            VLAN_ANY,
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "any",
            },
        ]
        self.assertEqual(
            self.client.endpoints,
            [
                VLAN_ANY,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "any",
                },
            ],
        )

    def test_endpoints_vlan_any_mixed(self):
        """Checks that setting VLAN to 'any' with other specific VLAN IDs works."""
        self.client.endpoints = [
            VLAN_ANY,
            VLAN_200,
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
            self.client.endpoints,
            [
                VLAN_ANY,
                VLAN_200,
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
        self.assert_invalid_endpoints(
            [
                VLAN_ANY,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "5000",
                },
            ],
            ERROR_INVALID_VLAN_VALUE.format("5000"),
        )

    # VLAN value "untagged" #
    def test_endpoints_vlan_untagged_single(self):
        """Checks that setting a VLAN to 'untagged' for a single endpoint works."""
        self.client.endpoints = [VLAN_UNTAGGED, VLAN_200]
        self.assertEqual(self.client.endpoints, [VLAN_UNTAGGED, VLAN_200])

    def test_endpoints_vlan_untagged_multiple(self):
        """Checks that setting VLAN to 'untagged' for multiple endpoints works."""
        self.client.endpoints = [
            VLAN_UNTAGGED,
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "untagged",
            },
        ]
        self.assertEqual(
            self.client.endpoints,
            [
                VLAN_UNTAGGED,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "untagged",
                },
            ],
        )

    def test_endpoints_vlan_untagged_mixed(self):
        """Checks that setting VLAN to 'untagged' with other specific VLAN IDs works."""
        self.client.endpoints = [
            VLAN_UNTAGGED,
            VLAN_200,
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
            self.client.endpoints,
            [
                VLAN_UNTAGGED,
                VLAN_200,
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
        self.assert_invalid_endpoints(
            [
                VLAN_UNTAGGED,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "5000",
                },
            ],
            ERROR_INVALID_VLAN_VALUE.format("5000"),
        )

    # VLAN range #
    def test_endpoints_vlan_range_valid(self):
        """Checks that setting a valid VLAN range works."""
        self.client.endpoints = [
            VLAN_RANGE,
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "100:200",
            },
        ]
        self.assertEqual(
            self.client.endpoints,
            [
                VLAN_RANGE,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "100:200",
                },
            ],
        )

    def test_endpoints_vlan_range_empty_vlan_value(self):
        """Checks that each endpoint's 'vlan' key cannot be empty when used with range."""
        self.assert_invalid_endpoints(
            [
                VLAN_RANGE,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "",
                },
            ],
            ERROR_EMPTY_VLAN_VALUE,
        )

    def test_endpoints_vlan_range_mismatch(self):
        """Checks that setting a VLAN range for one endpoint and a different range for another raised a ValueError."""
        self.assert_invalid_endpoints(
            [
                VLAN_RANGE,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200:300",
                },
            ],
            ERROR_VLAN_RANGE_MISMATCH,
        )

    def test_endpoints_vlan_range_single_endpoint(self):
        """Checks that setting a VLAN range for one endpoint and a single VLAN for another raises a ValueError."""
        self.assert_invalid_endpoints(
            [
                VLAN_RANGE,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "300",
                },
            ],
            ERROR_VLAN_RANGE_MISMATCH,
        )

    def test_endpoints_vlan_range_invalid_endpoint(self):
        """Checks that setting a VLAN range for one endpoint and an invlaid value for another raises a ValueError."""
        self.assert_invalid_endpoints(
            [
                VLAN_RANGE,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "invalid value",
                },
            ],
            ERROR_VLAN_INVALID.format("invalid value"),
        )

    def test_endpoints_vlan_range_and_any(self):
        """Checks that setting a VLAN range and 'any' raises a ValueError."""
        self.assert_invalid_endpoints(
            [
                VLAN_RANGE,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "any",
                },
            ],
            ERROR_VLAN_RANGE_MISMATCH,
        )

    def test_endpoints_vlan_range_and_untagged(self):
        """Checks that setting a VLAN range and 'untagged' raises a ValueError."""
        self.assert_invalid_endpoints(
            [
                VLAN_RANGE,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "untagged",
                },
            ],
            ERROR_VLAN_RANGE_MISMATCH,
        )

    def test_endpoints_vlan_range_and_all(self):
        """Checks that setting a VLAN range and 'all' raises a ValueError."""
        self.assert_invalid_endpoints(
            [
                VLAN_RANGE,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "all",
                },
            ],
            ERROR_VLAN_RANGE_MISMATCH,
        )

    def test_endpoints_vlan_range_invalid_format(self):
        """Checks that setting an invalid VLAN range raises a ValueError."""
        self.assert_invalid_endpoints(
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200:100",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "200:100",
                },
            ],
            ERROR_VLAN_RANGE_VALUE.format("200:100"),
        )

    def test_endpoints_vlan_range_out_of_bounds_0(self):
        """Checks that setting a VLAN range out of the lower bound raises a ValueError."""
        self.assert_invalid_endpoints(
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "0:200",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "0:200",
                },
            ],
            ERROR_VLAN_RANGE_VALUE.format("0:200"),
        )

    def test_endpoints_vlan_range_out_of_bounds_4096(self):
        """Checks that setting a VLAN range out of the upper bould raises a ValueError."""
        self.assert_invalid_endpoints(
            [
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "4000:4096",
                },
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "4000:4096",
                },
            ],
            ERROR_VLAN_RANGE_VALUE.format("4000:4096"),
        )

    def test_endpoints_vlan_range_and_invalid_vlan(self):
        """Checks that setting a VLAN range and an invalid VLAN value raises a ValueError."""
        self.assert_invalid_endpoints(
            [
                VLAN_RANGE,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "5000",
                },
            ],
            ERROR_INVALID_VLAN_VALUE.format("5000"),
        )

    # VLAN value "all" #
    def test_endpoints_vlan_all_valid(self):
        """Checks that setting a VLAN to 'all' for a single endpoint works if all endpoints have 'all'."""
        self.client.endpoints = [
            VLAN_ALL,
            {
                "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name2",
                "vlan": "all",
            },
        ]
        self.assertEqual(
            self.client.endpoints,
            [
                VLAN_ALL,
                {
                    "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name2",
                    "vlan": "all",
                },
            ],
        )

    def test_endpoints_vlan_intger(self):
        """Checks that setting a VLAN to 'all' with other VLAN values raises a ValueError."""
        self.assert_invalid_endpoints([VLAN_ALL, VLAN_200,], ERROR_VLAN_RANGE_MISMATCH)

    def test_endpoints_vlan_all_any(self):
        """Checks that setting a VLAN to 'all' with 'any' raises a ValueError."""
        self.assert_invalid_endpoints(
            [
                VLAN_ALL,
                {
                    "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name2",
                    "vlan": "any",
                },
            ],
            ERROR_VLAN_RANGE_MISMATCH,
        )

    def test_endpoints_vlan_all_untagged(self):
        """Checks that setting a VLAN to 'all' with 'untagged' raises a ValueError."""
        self.assert_invalid_endpoints(
            [
                VLAN_ALL,
                {
                    "port_id": "urn:sdx:port:test-ox_url:test-node_name:test-port_name2",
                    "vlan": "untagged",
                },
            ],
            ERROR_VLAN_RANGE_MISMATCH,
        )

    # Other VLAN value tests #
    def test_endpoints_valid_vlan_format(self):
        """Checks that the 'vlan' key follows the required format."""
        self.assert_invalid_endpoints(
            [
                VLAN_100,
                {
                    "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                    "vlan": "invalid_vlan",
                },
            ],
            ERROR_VLAN_INVALID.format("invalid_vlan"),
        )

    def test_valid_endpoints(self):
        """Checks that valid endpoints are accepted."""
        valid_endpoints = [VLAN_100, VLAN_200]
        self.client.endpoints = valid_endpoints
        self.assertEqual(self.client.endpoints, valid_endpoints)


# Run the tests
if __name__ == "__main__":
    unittest.main()
