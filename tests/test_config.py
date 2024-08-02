from sdxlib.sdx_client import SDXClient

TEST_URL = "http://example.com"
TEST_NAME = "Test L2VPN"
TEST_ENDPOINTS = [
    {
        "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
        "vlan": "100",
    },
    {
        "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
        "vlan": "200",
    },
]

ERROR_NAME_INVALID= "Name must be a non-empty string with maximum 50 characters."
ERROR_ENDPOINTS_LIST = "Endpoints must be a list."
ERROR_ENDPOINTS_MIN_ENTRIES = "Endpoints must contain at least 2 entries."
ERROR_ENDPOINTS_LIST_DICTS = "Endpoints must be a list of dictionaries."
ERROR_ENDPOINTS_VLAN_SAME = "All endpoints must have the same VLAN value is one endpoint is 'all' or a range."
ERROR_ENDPOINTS_INVALID_VLAN = "Invalid VLAN value: '{}'. Must be 'any', 'all', 'untagged', a string representing an integer between 1 and 4095, or a range."

def create_client(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS):
    return SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)