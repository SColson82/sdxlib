import unittest
from sdxlib.sdx_client import SDXClient
from test_config import TEST_URL, TEST_NAME, TEST_ENDPOINTS

class TestSDXClient(unittest.TestCase):
    def test_name_empty_string(self):
        """Checks that empty string is not allowed for 'name' attribute."""
        client = SDXClient(
            base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS
        )
        with self.assertRaises(ValueError) as context:
            client.name = ""
        self.assertEqual(
            str(context.exception),
            "Name must be a non-empty string with maximum 50 characters.",
        )

    def test_name_too_long(self):
        """Checks that the 'name' exceeding 50 characters is not allowed."""
        client = SDXClient(
            base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS
        )
        with self.assertRaises(ValueError) as context:
            client.name = "This is a very long name that exceeds 50 chatacters limit"
        self.assertEqual(
            str(context.exception),
            "Name must be a non-empty string with maximum 50 characters.",
        )

    def test_name_non_string(self):
        """Checks that a non-string value is not allowed for the 'name' attribute."""
        client = SDXClient(base_url=TEST_URL, endpoints=TEST_ENDPOINTS)
        with self.assertRaises(ValueError) as context:
            client.name = 123
        self.assertEqual(
            str(context.exception),
            "Name must be a non-empty string with maximum 50 characters.",
        )

    def test_valid_name(self):
        """Checks that a valid name is accepted."""
        client = SDXClient(
            base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS
        )
        self.assertEqual(client.name, "Test L2VPN")

# Run the tests
if __name__ == "__main__":
    unittest.main()
