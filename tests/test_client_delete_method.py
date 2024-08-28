import requests
import unittest
from unittest.mock import patch, Mock
from sdxlib.sdx_client import SDXClient
from sdxlib.sdx_exception import SDXException
from requests.exceptions import HTTPError, Timeout, RequestException
from test_config import TEST_URL, TEST_NAME, TEST_ENDPOINTS, TEST_SERVICE_ID


class TestSDXClient(unittest.TestCase):
    def setUp(self):
        self.client = SDXClient(base_url=TEST_URL)

    # Successful Deletion
    @patch("requests.delete")
    def test_delete_l2vpn_success(self, mock_delete):
        """Test successful deletion of an L2VPN."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.content = ""
        mock_response.json.return_value = {}

        mock_delete.return_value = mock_response

        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS,)

        result = client.delete_l2vpn(TEST_SERVICE_ID)
        self.assertIsNone(result)
        mock_delete.assert_called_with(
            f"{TEST_URL}/l2vpn/1.0/{TEST_SERVICE_ID}", verify=True, timeout=120
        )

    # Unauthorized error (401)
    @patch("requests.delete")
    def test_delete_l2vpn_401_error(self, mock_delete):
        """Test handling of 401 error for L2VPN deletion."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_delete.return_value = mock_response

        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS,)

        with self.assertRaises(SDXException):
            client.delete_l2vpn(TEST_SERVICE_ID)

    # Not found error (404)
    @patch("requests.delete")
    def test_delete_l2vpn_404_error(self, mock_delete):
        """Test handling of 404 error for L2VPN deletion."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_delete.return_value = mock_response

        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS,)

        with self.assertRaises(SDXException):
            client.delete_l2vpn(TEST_SERVICE_ID)

    # Logging success
    @patch("requests.delete")
    @patch("logging.getLogger")
    def test_delete_l2vpn_logging_success(self, mock_get_logger, mock_delete):
        """Test logging of successful L2VPN deletion."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_delete.return_value = mock_response

        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            logger=mock_logger,
        )

        client.delete_l2vpn(TEST_SERVICE_ID)
        mock_get_logger().info.assert_called_with(
            f"L2VPN deletion request sent to {TEST_URL}/l2vpn/1.0/{TEST_SERVICE_ID}."
        )

    # Logging Error Conditions
    @patch("requests.delete")
    @patch("logging.getLogger")
    def test_delete_l2vpn_logging_error_conditions(self, mock_get_logger, mock_delete):
        """Test logging of error conditions for L2VPN deletion."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"description": "Service ID not found"}
        mock_delete.side_effect = HTTPError(response=mock_response)

        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            logger=mock_logger,
        )

        with self.assertRaises(SDXException):
            client.delete_l2vpn(TEST_SERVICE_ID)
        mock_logger.error.assert_called_with(
            "Failed to delete L2VPN. Status code: 404: Service ID not found"
        )

    # Request exceptions
    @patch("requests.delete")
    def test_delete_l2vpn_request_exception(self, mock_delete):
        """Test handling of request exceptions during L2VPN deletion."""
        mock_delete.side_effect = RequestException("Network error")

        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS,)

        with self.assertRaises(SDXException):
            client.delete_l2vpn(TEST_SERVICE_ID)

    # Handle no content
    @patch("requests.delete")
    def test_delete_l2vpn_no_content(self, mock_delete):
        """Test handling of response with no content for L2VPN deletion."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.content = b""
        mock_delete.return_value = mock_response

        client = SDXClient(base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS,)

        result = client.delete_l2vpn(TEST_SERVICE_ID)
        self.assertIsNone(result)

    # Verify Correct Exception Handling for Non-HTTPError Exceptions
    @patch("requests.delete")
    @patch("logging.getLogger")
    def test_delete_l2vpn_general_request_exception(self, mock_get_logger, mock_delete):
        """Test handling of general RequestException during L2VPN deletion."""
        mock_delete.side_effect = RequestException("Network error")

        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            logger=mock_logger,
        )

        with self.assertRaises(SDXException):
            client.delete_l2vpn(TEST_SERVICE_ID)

        mock_logger.error.assert_called_with("Failed to delete L2VPN: Network error")

    # Ensure Error Messages for All Status Codes
    @patch("requests.delete")
    def test_delete_l2vpn_error_messages(self, mock_delete):
        """Test error messages for different status codes during L2VPN deletion."""
        for status_code, expected_message in {
            401: "Not Authorized",
            404: "L2VPN Service ID provided does not exist",
            500: "Unknown error",
        }.items():
            mock_response = Mock()
            mock_response.status_code = status_code
            mock_response.json.return_value = {"description": expected_message}
            mock_response.raise_for_status.side_effect = HTTPError(
                response=mock_response
            )
            mock_delete.return_value = mock_response

            client = SDXClient(
                base_url=TEST_URL, name=TEST_NAME, endpoints=TEST_ENDPOINTS,
            )

            with self.assertRaises(SDXException) as cm:
                client.delete_l2vpn(TEST_SERVICE_ID)

            self.assertEqual(cm.exception.message, expected_message)

    @patch("requests.delete", side_effect=Timeout)
    @patch("logging.getLogger")
    def test_delete_l2vpn_timeout_logging(self, mock_get_logger, mock_delete):
        """Test logging of timeout exception during L2VPN deletion."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            logger=mock_logger,
        )

        with self.assertRaises(SDXException):
            client.delete_l2vpn(TEST_SERVICE_ID)

        # Assert that the error was logged
        mock_logger.error.assert_called_with("Request timed out.")


# Run the tests
if __name__ == "__main__":
    unittest.main()
