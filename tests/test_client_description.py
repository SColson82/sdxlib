import unittest
from sdxlib.sdx_client import SDXClient
from test_config import TEST_URL, TEST_NAME, TEST_ENDPOINTS

class TestSDXClient(unittest.TestCase):
    # Unit Tests for Description Attribute(Optional) #
    def test_set_valid_description(self):
        """Test setting a valid 'description' value of string."""
        client = SDXClient(
            base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS
        )
        valid_description = "This is a valid description."
        client.description = valid_description
        self.assertEqual(client.description, valid_description)

    def test_set_valid_description_url(self):
        """Test setting a valid 'description' value of URL."""
        client = SDXClient(
            base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS
        )
        valid_description = "https://example.com/info"
        client.description = valid_description
        self.assertEqual(client.description, valid_description)

    def test_set_description_none(self):
        """Test setting the description to None."""
        client = SDXClient(
            base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS
        )
        client.description = None
        self.assertIsNone(client.description)

    def test_set_description_exceeding_limit(self):
        """Test setting description exceeding 255-character limit will raise ValueError"""
        client = SDXClient(
            base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS
        )
        long_description = "x" * 256
        with self.assertRaises(ValueError) as context:
            client.description = long_description
        self.assertEqual(
            str(context.exception),
            "Description attribute must be less than 256 characters.",
        )

# Run the tests
if __name__ == "__main__":
    unittest.main()
