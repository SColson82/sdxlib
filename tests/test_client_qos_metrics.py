import unittest
from sdxlib.sdx_client import SDXClient
from test_config import create_client


class TestSDXClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client = create_client()

    def test_qos_metrics_none(self):
        """Test setting qos_metrics to None"""
        self.assertIsNone(self.client.qos_metrics)

    def assert_invalid_qos_metrics(
        self, invalid_value, expected_message, exception=ValueError
    ):
        with self.assertRaises(exception) as context:
            self.client.qos_metrics = invalid_value
        self.assertEqual(str(context.exception), expected_message)

    def test_qos_metrics_empty_dict(self):
        """Test setting qos_metrics to an empty dictionary"""
        self.client.qos_metrics = {}
        self.assertIsNone(self.client.qos_metrics)

    def test_qos_metrics_valid(self):
        """Test setting qos_metrics with valid data"""
        client_qos_metrics = {
            "min_bw": {"value": 10, "strict": False},
            "max_delay": {"value": 200, "strict": True},
        }
        self.client.qos_metrics = client_qos_metrics
        self.assertEqual(self.client.qos_metrics, client_qos_metrics)

    def test_qos_metrics_invalid_type(self):
        """Test setting qos_metrics with invalid type"""
        invalid_value = "invalid string"
        self.assert_invalid_qos_metrics(
            invalid_value, "QoS metrics must be a dictionary.", TypeError
        )

    def test_qos_metrics_min_bw_out_of_range(self):
        """Test setting min_bw with value outside valid range"""
        invalid_value = {"min_bw": {"value": -10, "strict": False}}
        self.assert_invalid_qos_metrics(
            invalid_value, "qos_metric 'min_bw' value must be between 0 and 100."
        )


# Run the tests
if __name__ == "__main__":
    unittest.main()
