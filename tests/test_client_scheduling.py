import unittest
from sdxlib.sdx_client import SDXClient
from test_config import TEST_URL, TEST_NAME, TEST_ENDPOINTS


class TestSDXClientScheduling(unittest.TestCase):
    def test_valid_scheduling_both_times(self):
        client_description = (
            "This is an example to demonstrate a L2VPN with optional attributes."
        )
        client_notifications = [{"email": f"user{i+1}@email.com"} for i in range(10)]
        client_scheduling = {
            "start_time": "2024-07-04T10:00:00Z",
            "end_time": "2024-07-05T18:00:00Z",
        }
        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            description=client_description,
            notifications=client_notifications,
            scheduling=client_scheduling,
        )
        self.assertEqual(
            client.scheduling,
            {"start_time": "2024-07-04T10:00:00Z", "end_time": "2024-07-05T18:00:00Z"},
        )

    def test_valid_scheduling_end_time_only(self):
        client_scheduling = {"end_time": "2024-07-05T18:00:00Z"}
        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            scheduling=client_scheduling,
        )
        self.assertEqual(client.scheduling, {"end_time": "2024-07-05T18:00:00Z"})

    def test_valid_scheduling_empty_dict(self):
        client = SDXClient(
            base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS, scheduling={},
        )
        self.assertEqual(client.scheduling, None)

    def test_invalid_scheduling_format(self):
        with self.assertRaises(ValueError) as context:
            SDXClient(
                base_url=TEST_URL,
                name=TEST_NAME,
                endpoints=TEST_ENDPOINTS,
                scheduling={"start_time": "invalid format"},
            )
        self.assertEqual(
            str(context.exception),
            "Invalid 'start_time' format. Use ISO8601 format (YYYY-MM-DDTHH:mm:SSZ).",
        )

    def test_invalid_scheduling_end_before_start(self):
        with self.assertRaises(ValueError) as context:
            SDXClient(
                base_url=TEST_URL,
                name=TEST_NAME,
                endpoints=TEST_ENDPOINTS,
                scheduling={
                    "start_time": "2024-07-05T18:00:00Z",
                    "end_time": "2024-07-05T10:00:00Z",
                },
            )
        self.assertEqual(str(context.exception), "End time must be after start time.")

    def test_invalid_scheduling_data_type(self):
        with self.assertRaises(TypeError) as context:
            SDXClient(
                base_url=TEST_URL,
                name=TEST_NAME,
                endpoints=TEST_ENDPOINTS,
                scheduling="not a dictionary",
            )
        self.assertEqual(
            str(context.exception), "Scheduling attribute must be a dictionary."
        )


if __name__ == "__main__":
    unittest.main()
