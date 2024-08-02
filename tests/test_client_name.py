import unittest
from sdxlib.sdx_client import SDXClient
from test_config import TEST_URL, TEST_NAME, TEST_ENDPOINTS


class TestSDXClient(unittest.TestCase):
    ERROR_MESSAGE = "Name must be a non-empty string with maximum 50 characters."
    def setUp(self):
        """Initializes the client instance."""
        self.client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)

    def assert_invalid_name(self, invalid_name):
        """Helper function to assert a ValueError with a specific message."""
        with self.assertRaises(ValueError) as context:
            self.client.name = invalid_name
        self.assertEqual(str(context.exception), self.ERROR_MESSAGE)

    # Checks for no name passed.
    def test_name_empty_string(self):
        """Checks that empty string is not allowed for 'name' attribute."""
        self.assert_invalid_name("")
         
    # Checks for multiple whitestrings passed.
    def test_name_whitespace_string(self):
        """Checks that a whitespace string is not allowed for 'name' attribute."""
        self.assert_invalid_name("       ")

    # Checks for non-string name.
    def test_name_non_string(self):
        """Checks that a non-string value is not allowed for the 'name' attribute."""
        self.assert_invalid_name(123)
 
    # Checks for name longer than 50 characters.
    def test_name_too_long(self):
        """Checks that the 'name' exceeding 50 characters is not allowed."""
        self.assert_invalid_name("This is a very long name that exceeds 50 characters limit.")

    # Checks for exactly 50 characters passed.
    def test_name_max_length(self):
        """Checks that a 'name' of exactly 50 characters is allowed."""
        max_length_name = "a" * 50
        self.client.name = max_length_name
        self.assertEqual(self.client.name, max_length_name)

    # Checks for valid name passes. 
    def test_valid_name(self):
        """Checks that a valid name is accepted."""
        self.assertEqual(self.client.name, "Test L2VPN")

# Run the tests
if __name__ == "__main__":
    unittest.main()
