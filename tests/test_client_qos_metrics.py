import unittest
from sdxlib.sdx_client import SDXClient


class TestSDXClient(unittest.TestCase):
    def test_qos_metrics_none(self):
        """Test setting qos_metrics to None"""
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
            base_url="http://example.com",
            name="test",
            endpoints=client_endpoints,
            description="",
        )
        self.assertIsNone(client.qos_metrics)

    def test_qos_metrics_empty_dict(self):
        """Test setting qos_metrics to an empty dictionary"""
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
            base_url="http://example.com",
            name="test",
            endpoints=client_endpoints,
            description="",
            qos_metrics={},
        )
        self.assertIsNone(client.qos_metrics)

    def test_qos_metrics_valid(self):
        """Test setting qos_metrics with valid data"""
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
        client_qos_metrics = {
            "min_bw": {"value": 10, "strict": False},
            "max_delay": {"value": 200, "strict": True},
        }
        client = SDXClient(
            base_url="http://example.com",
            name="test",
            endpoints=client_endpoints,
            description="",
            qos_metrics=client_qos_metrics,
        )
        self.assertEqual(client.qos_metrics, client_qos_metrics)

    def test_qos_metrics_invalid_type(self):
        """Test setting qos_metrics with invalid type"""
        client_url = "http://example.com"
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
        client = SDXClient(base_url=client_url, name=client_name, endpoints=client_endpoints)
        with self.assertRaises(TypeError) as context:
                client.qos_metrics = "invalid string",
        self.assertEqual(
            str(context.exception), "QoS metrics must be a dictionary."
        )

    def test_qos_metrics_min_bw_out_of_range(self):
        """Test setting min_bw with value outside valid range"""
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
        with self.assertRaises(ValueError) as context:
            qos_metrics = {
                "min_bw": {"value": -10, "strict": False}
            }  # Negative value for min_bw
            SDXClient(
                base_url="http://example.com",
                name="test",
                endpoints=client_endpoints,
                description="",
                qos_metrics=qos_metrics,
            )
        self.assertEqual(
            str(context.exception),
            "qos_metric 'min_bw' value must be between 0 and 100.",
        )


# Run the tests
if __name__ == "__main__":
    unittest.main()
