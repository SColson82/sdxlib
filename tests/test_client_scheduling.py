import unittest
from sdxlib.sdx_client import SDXClient


class TestSDXClientScheduling(unittest.TestCase):
    def test_valid_scheduling_both_times(self):
        client_name = "Test"
        client_endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100:200",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "100:200",
            },
        ]
        client_description = (
            "This is an example to demonstrate a L2VPN with optional attributes."
        )
        client_notifications = [{"email": f"user{i+1}@email.com"} for i in range(10)]
        client_scheduling = {
            "start_time": "2024-07-04T10:00:00Z",
            "end_time": "2024-07-05T18:00:00Z",
        }
        client = SDXClient(
            base_url="http://example.com",
            name=client_name,
            endpoints=client_endpoints,
            description=client_description,
            notifications=client_notifications,
            scheduling=client_scheduling,
        )
        self.assertEqual(
            client.scheduling,
            {"start_time": "2024-07-04T10:00:00Z", "end_time": "2024-07-05T18:00:00Z"},
        )

    def test_valid_scheduling_end_time_only(self):
        client_name = "Test"
        client_endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100:200",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "100:200",
            },
        ]
        client_scheduling = {"end_time": "2024-07-05T18:00:00Z"}
        client = SDXClient(
            base_url="http://example.com",
            name=client_name,
            endpoints=client_endpoints,
            scheduling=client_scheduling,
        )
        self.assertEqual(client.scheduling, {"end_time": "2024-07-05T18:00:00Z"})

    def test_valid_scheduling_empty_dict(self):
        client_name = "Test"
        client_endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100:200",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "100:200",
            },
        ]
        client = SDXClient(
            base_url="http://example.com",
            name=client_name,
            endpoints=client_endpoints,
            scheduling={},
        )
        self.assertEqual(client.scheduling, None)

    def test_invalid_scheduling_format(self):
        client_name = "Test"
        client_endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100:200",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "100:200",
            },
        ]
        with self.assertRaises(ValueError) as context:
            client = SDXClient(
                base_url="http://example.com",
                name=client_name,
                endpoints=client_endpoints,
                scheduling={"start_time": "invalid format"},
            )
        self.assertEqual(
            str(context.exception),
            "Invalid 'start_time' format. Use ISO8601 format (YYYY-MM-DDTHH:mm:SSZ).",
        )

    def test_invalid_scheduling_end_before_start(self):
        client_name = "Test"
        client_endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100:200",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "100:200",
            },
        ]
        with self.assertRaises(ValueError) as context:
            client = SDXClient(
                base_url="http://example.com",
                name=client_name,
                endpoints=client_endpoints,
                scheduling={
                    "start_time": "2024-07-05T18:00:00Z",
                    "end_time": "2024-07-05T10:00:00Z",
                },
            )
        self.assertEqual(str(context.exception), "End time must be after start time.")

    def test_invalid_scheduling_data_type(self):
        client_name = "Test"
        client_endpoints = [
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
                "vlan": "100:200",
            },
            {
                "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
                "vlan": "100:200",
            },
        ]
        with self.assertRaises(TypeError) as context:
            client = SDXClient(
                base_url="http://example.com",
                name=client_name,
                endpoints=client_endpoints,
                scheduling="not a dictionary",
            )
        self.assertEqual(
            str(context.exception), "Scheduling attribute must be a dictionary."
        )


if __name__ == "__main__":
    unittest.main()
