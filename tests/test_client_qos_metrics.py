import unittest
from sdxlib.sdx_client import SDXClient
from test_config import TEST_URL, TEST_NAME, TEST_ENDPOINTS

class TestSDXClient(unittest.TestCase):
    def test_qos_metrics_none(self):
        """Test setting qos_metrics to None"""
        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            description="",
        )
        self.assertIsNone(client.qos_metrics)

    def test_qos_metrics_empty_dict(self):
        """Test setting qos_metrics to an empty dictionary"""
        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            description="",
            qos_metrics={},
        )
        self.assertIsNone(client.qos_metrics)

    def test_qos_metrics_valid(self):
        """Test setting qos_metrics with valid data"""
        client_qos_metrics = {
            "min_bw": {"value": 10, "strict": False},
            "max_delay": {"value": 200, "strict": True},
        }
        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            description="",
            qos_metrics=client_qos_metrics,
        )
        self.assertEqual(client.qos_metrics, client_qos_metrics)

    def test_qos_metrics_invalid_type(self):
        """Test setting qos_metrics with invalid type"""
        client = SDXClient(
            base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS
        )
        with self.assertRaises(TypeError) as context:
            client.qos_metrics = ("invalid string",)
        self.assertEqual(str(context.exception), "QoS metrics must be a dictionary.")

    def test_qos_metrics_min_bw_out_of_range(self):
        """Test setting min_bw with value outside valid range"""
        with self.assertRaises(ValueError) as context:
            qos_metrics = {
                "min_bw": {"value": -10, "strict": False}
            }  # Negative value for min_bw
            SDXClient(
                base_url=TEST_URL,
                name=TEST_NAME,
                endpoints=TEST_ENDPOINTS,
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
