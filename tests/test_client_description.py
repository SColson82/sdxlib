import unittest
from sdxlib.sdx_client import SDXClient
from test_config import create_client, ERROR_DESCRIPTION_TOO_LONG


class TestSDXClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client = create_client()

    def assert_invalid_description(
        self, invalid_value, expected_message, exception=ValueError
    ):
        with self.assertRaises(exception) as context:
            self.client.description = invalid_value
        self.assertEqual(str(context.exception), expected_message)

    # Unit Tests for Description Attribute(Optional) #
    def test_set_valid_description(self):
        """Test setting a valid 'description' value of string."""
        valid_description = "This is a valid description."
        self.client.description = valid_description
        self.assertEqual(self.client.description, valid_description)

    def test_set_valid_description_url(self):
        """Test setting a valid 'description' value of URL."""
        valid_description = "https://example.com/info"
        self.client.description = valid_description
        self.assertEqual(self.client.description, valid_description)

    def test_set_description_none(self):
        """Test setting the description to None."""
        self.client.description = None
        self.assertIsNone(self.client.description)

    def test_set_description_exceeding_limit(self):
        """Test setting description exceeding 255-character limit will raise ValueError"""
        self.assert_invalid_description("x" * 256, ERROR_DESCRIPTION_TOO_LONG)


# Run the tests
if __name__ == "__main__":
    unittest.main()
