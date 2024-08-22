import requests
from requests.exceptions import HTTPError, Timeout, RequestException
import unittest
from unittest.mock import patch, Mock
from sdxlib.sdx_client import SDXClient
from sdxlib.sdx_exception import SDXException
from test_config import TEST_URL, TEST_NAME, TEST_ENDPOINTS


class TestSDXClient(unittest.TestCase):
    # # API Call Succeeds
    @patch("requests.post")
    @patch("logging.getLogger")
    def test_create_l2vpn_success_with_logging(self, mock_get_logger, mock_post):
        """Tests successful L2VPN creation and logging."""
        mock_response = Mock()
        mock_response.json.return_value = {"service_id": "123"}
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            description="Test Description",
            logger=mock_logger,
        )
        response = client.create_l2vpn()
        self.assertEqual(response, {"service_id": "123"})
        mock_post.assert_called_once_with(
            f"{TEST_URL}/l2vpn/1.0",
            json={
                "name": TEST_NAME,
                "endpoints": TEST_ENDPOINTS,
                "description": "Test Description",
            },
            timeout=120,
        )
        mock_logger.debug.assert_called_once_with(
            "Sending request to create L2VPN with payload: %s",
            {
                "name": TEST_NAME,
                "endpoints": TEST_ENDPOINTS,
                "description": "Test Description",
            },
        )
        mock_logger.info.assert_called_once_with(
            "L2VPN created successfully with service_id: 123"
        )

    @patch("requests.post")
    def test_create_l2vpn_error(self, mock_post):
        """Tests handling of RequestException during L2VPN creation."""
        # Set up mock error
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        # Create SDXClient object
        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS,)

        # Call the function and assert it raises SDXException
        with self.assertRaises(SDXException) as context:
            client.create_l2vpn()
        self.assertEqual(
            str(context.exception),
            "An error occurred while creating L2VPN: Connection error",
        )

        # Verify that requests.post was called
        mock_post.assert_called_once()

    def test_create_l2vpn_url_required(self):
        """Tests that base_url is required for L2VPN creation."""
        client = SDXClient(name=TEST_NAME, endpoints=TEST_ENDPOINTS,)
        with self.assertRaises(ValueError) as context:
            client.create_l2vpn()
        self.assertEqual(
            str(context.exception),
            "Creating L2VPN requires the base URL, name, and endpoints at minumum.",
        )

    def test_create_l2vpn_name_required(self):
        """Tests that name is required for L2VPN creation."""
        client = SDXClient(base_url=TEST_URL, endpoints=TEST_ENDPOINTS,)
        with self.assertRaises(ValueError) as context:
            client.create_l2vpn()
        self.assertEqual(
            str(context.exception),
            "Creating L2VPN requires the base URL, name, and endpoints at minumum.",
        )

    def test_create_l2vpn_endpoints_required(self):
        """Tests that endpoints are required for L2VPN creation."""
        with self.assertRaises(ValueError) as context:
            client = SDXClient(base_url=TEST_URL, name=TEST_NAME,)
            client.create_l2vpn()
        self.assertEqual(
            str(context.exception),
            "Creating L2VPN requires the base URL, name, and endpoints at minumum.",
        )

    def test_create_l2vpn_invalid_endpoints(self):
        """Tests handling of invalid endpoints type for L2VPN creation."""
        with self.assertRaises(TypeError) as context:
            client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints="invalid")
            client.create_l2vpn()
        self.assertEqual(str(context.exception), "Endpoints must be a list.")

    @patch("requests.post")
    def test_create_l2vpn_http_error(self, mock_post):
        """Tests handling of HTTP errors during L2VPN creation."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"description": "Bad Request"}
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)

        mock_post.return_value = mock_response

        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS)
        with self.assertRaises(SDXException) as context:
            client.create_l2vpn()
        self.assertEqual(
            str(context.exception),
            "Request does not have a valid JSON or body is incomplete/incorrect",
        )

    @patch("requests.post")
    @patch("logging.getLogger")
    def test_create_l2vpn_timeout_logging(self, mock_get_logger, mock_post):
        """Tests timeout handling and logging for L2VPN creation."""
        mock_post.side_effect = Timeout("Request timed out")
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            logger=mock_logger,
        )
        with self.assertRaises(SDXException) as context:
            client.create_l2vpn()
        self.assertEqual(
            str(context.exception), "The request to create the L2VPN timed out."
        )
        mock_logger.error.assert_called_once_with(
            "The request to create the L2VPN timed out."
        )

    @patch("requests.post")
    @patch("logging.getLogger")
    def test_create_l2vpn_request_exception_logging(self, mock_get_logger, mock_post):
        """Tests general request exception handling and logging for L2VPN creation."""
        mock_post.side_effect = RequestException("Connection error")
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            logger=mock_logger,
        )
        with self.assertRaises(SDXException) as context:
            client.create_l2vpn()
        self.assertEqual(
            str(context.exception),
            "An error occurred while creating L2VPN: Connection error",
        )
        mock_logger.error.assert_called_once_with(
            "An error occurred while creating L2VPN: Connection error"
        )

    @patch("requests.post")
    def test_create_l2vpn_caching(self, mock_post):
        """Tests caching mechanism by ensuring a single POST request is made."""
        mock_response = Mock()
        mock_response.json.return_value = {"service_id": "123"}
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            description="Test Description",
        )
        client.create_l2vpn()  # First call to populate the cache
        response = client.create_l2vpn()  # Second call should use the cache
        self.assertEqual(response, {"service_id": "123"})
        self.assertEqual(
            mock_post.call_count, 1
        )  # Ensure requests.post was only called once


# Run the tests
if __name__ == "__main__":
    unittest.main()
