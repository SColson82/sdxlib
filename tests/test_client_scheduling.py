import unittest
from sdxlib.sdx_client import SDXClient
from test_config import (
    create_client,
    ERROR_SCHEDULING_FORMAT,
    ERROR_SCHEDULING_END_BEFORE_START,
    ERROR_SCHEDULING_NOT_DICT,
)


class TestSDXClientScheduling(unittest.TestCase):
    def setUp(self) -> None:
        self.client = create_client(scheduling=None)

    def assert_invalid_scheduling(
        self, invalid_value, expected_message, exception=ValueError
    ):
        with self.assertRaises(exception) as context:
            self.client.scheduling = invalid_value
        self.assertEqual(str(context.exception), expected_message)

    def test_valid_scheduling_both_times(self):
        """Tests valid scheduling with both start and end times."""
        client_scheduling = {
            "start_time": "2024-07-04T10:00:00Z",
            "end_time": "2024-07-05T18:00:00Z",
        }
        self.client.scheduling = client_scheduling
        self.assertEqual(
            self.client.scheduling, client_scheduling,
        )

    def test_valid_scheduling_end_time_only(self):
        """Tests valid scheduling with only end time provided."""
        client_scheduling = {"end_time": "2024-07-05T18:00:00Z"}
        self.client.scheduling = client_scheduling
        self.assertEqual(self.client.scheduling, client_scheduling)

    def test_valid_scheduling_empty_dict(self):
        """Tests valid scheduling with an empty dictionary."""
        self.client.scheduling = {}
        self.assertEqual(self.client.scheduling, None)

    def test_invalid_scheduling_format(self):
        """Tests invalid scheduling format for start_time."""
        invalid_scheduling = {"start_time": "invalid format"}
        self.assert_invalid_scheduling(
            invalid_scheduling, ERROR_SCHEDULING_FORMAT,
        )

    def test_invalid_scheduling_end_before_start(self):
        """Tests invalid scheduling where end_time is before start_time."""
        invalid_scheduling = {
            "start_time": "2024-07-05T18:00:00Z",
            "end_time": "2024-07-05T10:00:00Z",
        }
        self.assert_invalid_scheduling(
            invalid_scheduling, ERROR_SCHEDULING_END_BEFORE_START
        )

    def test_invalid_scheduling_data_type(self):
        """Tests invalid scheduling data type (not a dictionary)."""
        invalid_scheduling = "not a dictionary"
        self.assert_invalid_scheduling(
            invalid_scheduling, ERROR_SCHEDULING_NOT_DICT, TypeError
        )


if __name__ == "__main__":
    unittest.main()
