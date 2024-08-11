# Successful object creation
mock_response_successful = {
    "service_id": "123e4567-e89b-12d3-a456-426614174000",
}

# Error Codes for SDXExceptions
mock_response_unsuccessful_400 = {
    "400": "Request does not have a valid JSON or body is incomplete/incorrect"
}
mock_response_unsuccessful_401 = {"401": "Not Authorized"}
mock_response_unsuccessful_402 = {
    "402": "Request not compatible (e.g., P2MP L2VPN requested, but only P2P supported)"
}
mock_response_unsuccessful_409 = {"409": "L2VPN Service already exists"}
mock_response_unsuccessful_410 = {"410": "Can't fulfill the strict QoS requirements"}
mock_response_unsuccessful_411 = {"411": "Scheduling not possible"}
mock_response_unsuccessful_422 = {"422": "Attribute not supported by the SDX-LC/OXPO"}
# Mock successful response
mock_response = {
    "service_id": "123e4567-e89b-12d3-a456-426614174000",
    "description": "L2VPN Service Modified",
}
# Define a mock response for no L2VPNs existing
mock_response_no_l2vpns = {}

# Define a mock response for one or more L2VPNs existing
mock_response_active_l2vpns_exist = {
    "c73da8e1-5d03-4620-a1db-7cdf23e8978c": {
        "service_id": "c73da8e1-5d03-4620-a1db-7cdf23e8978c",
        "name": "VLAN between AMPATH/300 and TENET/150",
        "endpoints": [
            {"port_id": "urn:sdx:port:tenet.ac.za:Tenet03:50", "vlan": "150"},
            {"port_id": "urn:sdx:port:ampath.net:Ampath3:50", "vlan": "300"},
        ],
        "description": "Example 1",
        "qos_metrics": {
            "min_bw": {"value": 5, "strict": False},
            "max_delay": {"value": 150, "strict": True},
        },
        "notifications": [{"email": "user@domain.com"}, {"email": "user2@domain2.com"}],
        "ownership": "user1",
        "creation_date": "20240522T00:00:00Z",
        "archived_date": "0",
        "status": "up",
        "state": "enabled",
        "counters_location": "https://my.aw-sdx.net/l2vpn/7cdf23e8978c",
        "last_modified": "0",
        "current_path": ["urn:sdx:link:tenet.ac.za:LinkToAmpath"],
        "oxp_service_ids": {"ampath.net": ["c73da8e1"], "Tenet.ac.za": ["5d034620"]},
    },
    "fa2c99ca-30a9-4b51-8491-683c52e326a6": {
        "service_id": "fa2c99ca-30a9-4b51-8491-683c52e326a6",
        "name": "Example 2",
        "endpoints": [
            {"port_id": "urn:sdx:port:tenet.ac.za:Tenet03:50", "vlan": "3500"},
            {"port_id": "urn:sdx:port:sax.br:router_01:50", "vlan": "3500"},
            {"port_id": "urn:sdx:port:ampath.net:Ampath3:50", "vlan": "3500"},
        ],
        "ownership": "user2",
        "creation_date": "20240422T00:00:00Z",
        "archived_date": "0",
        "status": "up",
        "state": "disabled",
        "counters_location": "https://my.aw-sdx.net/l2vpn/52e326a6",
        "last_modified": "0",
        "current_path": [
            "urn:sdx:link:tenet.ac.za:LinkToSAX",
            "urn:sdx:link:tenet.ac.za:LinkToAmpath",
            "urn:sdx:link:ampath.net:LinkToSAX",
        ],
        "oxp_service_ids": {
            "ampath.net": ["d82da7f9"],
            "tenet.ac.za": ["ab034673"],
            "sax.br": ["bb834633"],
        },
    },
}

# Define a mock response for one or more archived L2VPNs
mock_response_archived_l2vpns_exist = {
    "c73da8e1-5d03-4620-a1db-7cdf23e8978c": {
        "service_id": "c73da8e1-5d03-4620-a1db-7cdf23e8978c",
        "name": "VLAN between AMPATH/300 and TENET/150",
        "endpoints": [
            {"port_id": "urn:sdx:port:tenet.ac.za:Tenet03:50", "vlan": "150"},
            {"port_id": "urn:sdx:port:ampath.net:Ampath3:50", "vlan": "300"},
        ],
        "description": "Example 1",
        "qos_metrics": {
            "min_bw": {"value": 5, "strict": False},
            "max_delay": {"value": 150, "strict": True},
        },
        "notifications": [{"email": "user@domain.com"}, {"email": "user2@domain2.com"}],
        "ownership": "user1",
        "creation_date": "2024-05-22T00:00:00Z",
        "archived_date": "2024-06-16T19:20:30Z",
        "status": "up",
        "state": "enabled",
        "counters_location": "https://my.aw-sdx.net/l2vpn/7cdf23e8978c",
        "last_modified": "0",
        "current_path": ["urn:sdx:link:tenet.ac.za:LinkToAmpath"],
        "oxp_service_ids": {"ampath.net": ["c73da8e1"], "Tenet.ac.za": ["5d034620"]},
    },
    "fa2c99ca-30a9-4b51-8491-683c52e326a6": {
        "service_id": "fa2c99ca-30a9-4b51-8491-683c52e326a6",
        "name": "Example 2",
        "endpoints": [
            {"port_id": "urn:sdx:port:tenet.ac.za:Tenet03:50", "vlan": "3500"},
            {"port_id": "urn:sdx:port:sax.br:router_01:50", "vlan": "3500"},
            {"port_id": "urn:sdx:port:ampath.net:Ampath3:50", "vlan": "3500"},
        ],
        "ownership": "user2",
        "creation_date": "2024-05-22T00:00:00Z",
        "archived_date": "2024-06-16T19:20:30Z",
        "status": "up",
        "state": "disabled",
        "counters_location": "https://my.aw-sdx.net/l2vpn/52e326a6",
        "last_modified": "0",
        "current_path": [
            "urn:sdx:link:tenet.ac.za:LinkToSAX",
            "urn:sdx:link:tenet.ac.za:LinkToAmpath",
            "urn:sdx:link:ampath.net:LinkToSAX",
        ],
        "oxp_service_ids": {
            "ampath.net": ["d82da7f9"],
            "tenet.ac.za": ["ab034673"],
            "sax.br": ["bb834633"],
        },
    },
}
mock_response_all_archived_l2vpns = {
    "c73da8e1-5d03-4620-a1db-7cdf23e8978c": {
        "service_id": "c73da8e1-5d03-4620-a1db-7cdf23e8978c",
        "name": "VLAN between AMPATH/300 and TENET/150",
        "endpoints": [
            {"port_id": "urn:sdx:port:tenet.ac.za:Tenet03:50", "vlan": "150"},
            {"port_id": "urn:sdx:port:ampath.net:Ampath3:50", "vlan": "300"},
        ],
        "description": "Example 1",
        "qos_metrics": {
            "min_bw": {"value": 5, "strict": False},
            "max_delay": {"value": 150, "strict": True},
        },
        "notifications": [{"email": "user@domain.com"}, {"email": "user2@domain2.com"}],
        "ownership": "user1",
        "creation_date": "2024-05-22T00:00:00Z",
        "archived_date": "0",
        "status": "up",
        "state": "enabled",
        "counters_location": "https://my.aw-sdx.net/l2vpn/7cdf23e8978c",
        "last_modified": "0",
        "current_path": ["urn:sdx:link:tenet.ac.za:LinkToAmpath"],
        "oxp_service_ids": {"ampath.net": ["c73da8e1"], "Tenet.ac.za": ["5d034620"]},
    },
    "fa2c99ca-30a9-4b51-8491-683c52e326a6": {
        "service_id": "fa2c99ca-30a9-4b51-8491-683c52e326a6",
        "name": "Example 2",
        "endpoints": [
            {"port_id": "urn:sdx:port:tenet.ac.za:Tenet03:50", "vlan": "3500"},
            {"port_id": "urn:sdx:port:sax.br:router_01:50", "vlan": "3500"},
            {"port_id": "urn:sdx:port:ampath.net:Ampath3:50", "vlan": "3500"},
        ],
        "ownership": "user2",
        "creation_date": "2024-05-22T00:00:00Z",
        "archived_date": "2024-06-16T19:20:30Z",
        "status": "up",
        "state": "disabled",
        "counters_location": "https://my.aw-sdx.net/l2vpn/52e326a6",
        "last_modified": "0",
        "current_path": [
            "urn:sdx:link:tenet.ac.za:LinkToSAX",
            "urn:sdx:link:tenet.ac.za:LinkToAmpath",
            "urn:sdx:link:ampath.net:LinkToSAX",
        ],
        "oxp_service_ids": {
            "ampath.net": ["d82da7f9"],
            "tenet.ac.za": ["ab034673"],
            "sax.br": ["bb834633"],
        },
    },
}
# Define a mock response for one or more L2VPNs existing
mock_response_l2vpn_exists = {
    "c73da8e1-5d03-4620-a1db-7cdf23e8978c": {
        "service_id": "c73da8e1-5d03-4620-a1db-7cdf23e8978c",
        "name": "VLAN between AMPATH/300 and TENET/150",
        "endpoints": [
            {"port_id": "urn:sdx:port:tenet.ac.za:Tenet03:50", "vlan": "150"},
            {"port_id": "urn:sdx:port:ampath.net:Ampath3:50", "vlan": "300"},
        ],
        "description": "Example 1",
        "qos_metrics": {
            "min_bw": {"value": 5, "strict": False},
            "max_delay": {"value": 150, "strict": True},
        },
        "notifications": [{"email": "user@domain.com"}, {"email": "user2@domain2.com"}],
        "ownership": "user1",
        "creation_date": "20240522T00:00:00Z",
        "archived_date": "0",
        "status": "up",
        "state": "enabled",
        "counters_location": "https://my.aw-sdx.net/l2vpn/7cdf23e8978c",
        "last_modified": "0",
        "current_path": ["urn:sdx:link:tenet.ac.za:LinkToAmpath"],
        "oxp_service_ids": {"ampath.net": ["c73da8e1"], "Tenet.ac.za": ["5d034620"]},
    },
}
