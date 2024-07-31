import unittest
from sdxlib.sdx_client import SDXClient
from test_config import TEST_URL, TEST_NAME, TEST_ENDPOINTS


class TestSDXClient(unittest.TestCase):
    # Unit Tests for Notifications Attribute(Optional) #
    def test_notifications_valid(self):
        """Test setting and getting valid notifications within the 10-email limit."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
        valid_notifications = [
            {"email": "user1@email.com",},
            {"email": "user2@email.com",},
        ]
        client.notifications = valid_notifications
        self.assertEqual(client.notifications, valid_notifications)

    def test_notifications_not_list(self):
        """Test setting notifications with a non-list value, expecting a ValueError."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
        invalid_notifications = ({"email": "user1@email.com",},)
        with self.assertRaises(ValueError) as context:
            client.notifications = invalid_notifications
        self.assertEqual(
            str(context.exception), "Notifications must be provided as a list."
        )

    def test_notifications_list_element_not_dict(self):
        """Test setting notifications with a non-dictionary entry, expecting a ValueError."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
        invalid_notifications = [
            {"email": "user1@email.com",},
            "not a dict",
        ]
        with self.assertRaises(ValueError) as context:
            client.notifications = invalid_notifications
        self.assertEqual(
            str(context.exception), "Each notification must be a dictionary.",
        )

    def test_notifications_dict_no_email_key(self):
        """Test setting notification with a dictionary missing the 'email' key, expecting a ValueError."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
        invalid_notifications = [
            {"email": "user1@email.com",},
            {"not_email": "user2@email.com",},
        ]
        with self.assertRaises(ValueError) as context:
            client.notifications = invalid_notifications
        self.assertEqual(
            str(context.exception),
            "Each notification dictionary must contain a key 'email'.",
        )

    def test_notifications_dict_non_valid_email(self):
        """Test setting notifications with an invalid email format, expecting a ValueError."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
        invalid_notifications = [
            {"email": "user1@email.com",},
            {"email": "invalid_email",},
        ]
        with self.assertRaises(ValueError) as context:
            client.notifications = invalid_notifications
        self.assertEqual(
            str(context.exception),
            "Invalid email address or email format: invalid_email",
        )

    def test_notifications_list_too_long(self):
        """Test setting notifications exceeding 10-email limit, expecting a ValueError."""
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
        exceeding_notifications = [{"email": f"user{i}@email.com"} for i in range(11)]
        with self.assertRaises(ValueError) as context:
            client.notifications = exceeding_notifications
        self.assertEqual(
            str(context.exception),
            "Notifications can contain at most 10 email addresses.",
        )


# Run the tests
if __name__ == "__main__":
    unittest.main()
