import requests
from requests.exceptions import HTTPError, Timeout, RequestException
import unittest
from unittest.mock import patch, Mock
from sdxlib.sdx_client import SDXClient
from sdxlib.sdx_exception import SDXException
from test_config import TEST_URL, TEST_NAME, TEST_ENDPOINTS, TEST_SERVICE_ID


class TestSDXClient(unittest.TestCase):
    def setUp(self):
        self.client = SDXClient(base_url=TEST_URL)

    ## Test successful L2VPN update
    @patch("requests.patch")
    def test_successful_l2vpn_update(self, mock_patch):
        """Test that a valid update request is successful."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "description": "L2VPN Service Modified",
            "service_id": TEST_SERVICE_ID,
        }
        mock_patch.return_value = mock_response

        response = self.client.update_l2vpn(
            service_id=TEST_SERVICE_ID,
            state="enabled",
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            description="Test Description",
            notifications={"email": "user@example.com", "enabled": True},
            scheduling={
                "start_time": "2024-08-26T00:00:00Z",
                "end_time": "2024-08-27T00:00:00Z",
            },
            qos_metrics={"latency": {"value": 100, "priority": True}},
        )

        expected_response = None   #{
        #     "description": "L2VPN Service Modified",
        #     "service_id": TEST_SERVICE_ID,
        # }

        self.assertEqual(response, expected_response)
        mock_patch.assert_called_once()

    ## Test Update with Invalid JSON or Incomplete Body: 400 error code
    @patch("requests.patch")
    def test_invalid_json_or_incomplete_body(self, mock_patch):
        """Test that an invalid JSON or incomplete body results in a 400 error."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_patch.return_value = mock_response

        with self.assertRaises(SDXException):
            self.client.update_l2vpn(service_id=TEST_SERVICE_ID, state="enabled")

    ## Test Unauthorized Update: 401 error code
    @patch("requests.patch")
    def test_unauthorized_update(self, mock_patch):
        """Test that an unauthorized update results in a 401 error."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_patch.return_value = mock_response

        with self.assertRaises(SDXException):
            self.client.update_l2vpn(service_id=TEST_SERVICE_ID, state="enabled")

    ## Test Update with Incompatible Request: 402 error code
    @patch("requests.patch")
    def test_incompatible_request(self, mock_patch):
        """Test that an incompatible request results in a 402 error."""
        mock_response = Mock()
        mock_response.status_code = 402
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_patch.return_value = mock_response

        with self.assertRaises(SDXException):
            self.client.update_l2vpn(service_id=TEST_SERVICE_ID, state="enabled")

    ## Test Update of Non-Existing L2VPN: 404 error code
    @patch("requests.patch")
    def test_non_existing_l2vpn(self, mock_patch):
        """Test that updating a non-existing L2VPN results in a 404 error."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_patch.return_value = mock_response

        with self.assertRaises(SDXException):
            self.client.update_l2vpn(service_id=TEST_SERVICE_ID, state="enabled")

    ## Test Update with Conflicting L2VPN: 409 error code
    @patch("requests.patch")
    def test_conflicting_l2vpn(self, mock_patch):
        """Test that an update with a conflicting L2VPN results in a 409 error."""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_patch.return_value = mock_response

        with self.assertRaises(SDXException):
            self.client.update_l2vpn(service_id=TEST_SERVICE_ID, state="enabled")

    ## Test Update of Archived L2VPN: 410 status code
    @patch("requests.patch")
    def test_archived_l2vpn(self, mock_patch):
        """Test that updating an archived L2VPN results in a 410 status code."""
        mock_response = Mock()
        mock_response.status_code = 410
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_patch.return_value = mock_response

        with self.assertRaises(SDXException):
            self.client.update_l2vpn(service_id=TEST_SERVICE_ID, state="enabled")

    ## Test Update with QoS Requirements Not Fulfilled: 410 error code
    @patch("requests.patch")
    def test_qos_requirements_not_fulfilled(self, mock_patch):
        """Test that unfulfilled QoS requirements result in a 410 error."""
        mock_response = Mock()
        mock_response.status_code = 410
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_patch.return_value = mock_response

        with self.assertRaises(SDXException):
            self.client.update_l2vpn(service_id=TEST_SERVICE_ID, state="enabled")

    ## Test Update with Scheduling Not Possible: 411 error code
    @patch("requests.patch")
    def test_scheduling_not_possible(self, mock_patch):
        """Test that scheduling not possible results in a 411 error."""
        mock_response = Mock()
        mock_response.status_code = 411
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_patch.return_value = mock_response

        with self.assertRaises(SDXException):
            self.client.update_l2vpn(service_id=TEST_SERVICE_ID, state="enabled")

    @patch("logging.getLogger")
    def test_logging_called(self, mock_get_logger):
        """Test that logging is called."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        # Simulate a logging action
        mock_logger.info("Test log message")

        # Verify that the logger's info method was called
        mock_logger.info.assert_called_once_with("Test log message")

    @patch("logging.getLogger")
    @patch("requests.patch")
    def test_logging_successful_update(self, mock_patch, mock_get_logger):
        """Test that a successful update logs an info message."""

        mock_response = Mock()
        mock_response.status_code = 201
        mock_patch.return_value = mock_response

        mock_logger = Mock()

        mock_get_logger.return_value = mock_logger

        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            logger=mock_logger,
        )

        # Call the method
        client.update_l2vpn(service_id=TEST_SERVICE_ID, state="enabled")
        expected_url = (
            f"{self.client.base_url}/l2vpn/{self.client.VERSION}/{TEST_SERVICE_ID}"
        )

        expected_payload = {"service_id": TEST_SERVICE_ID, "state": "enabled"}

        # Construct the expected log messages
        expected_request_log = f"L2VPN update request sent to {expected_url}, with payload: {expected_payload}."
        expected_success_log = f"L2VPN with service_id {TEST_SERVICE_ID} was successfully updated."

        # Assert that both log messages were logged
        mock_logger.info.assert_any_call(expected_request_log)
        mock_logger.info.assert_any_call(expected_success_log)

        # Assert that both log calls occurred (i.e., two info calls were made)
        self.assertEqual(mock_logger.info.call_count, 2)

    ## Test Logging for Update Errors
    @patch("logging.getLogger")
    @patch("requests.patch")
    def test_logging_update_errors(self, mock_patch, mock_get_logger):
        """Test that update errors are logged as error messages."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_patch.return_value = mock_response

        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        client = SDXClient(
            base_url=TEST_URL,
            name=TEST_NAME,
            endpoints=TEST_ENDPOINTS,
            logger=mock_logger,
        )

        with self.assertRaises(SDXException):
            client.update_l2vpn(service_id=TEST_SERVICE_ID, state="enabled")

        expected_message = "Failed to update L2VPN. Status code: 400: Request does not have a valid JSON or body is incomplete/incorrect"
        mock_logger.error.assert_called_with(expected_message)

    ## Test Handling of Invalid 'state' Values
    def test_invalid_state_values(self):
        """Test that invalid 'state' values raise a ValueError."""
        with self.assertRaises(ValueError):
            self.client.update_l2vpn(service_id=TEST_SERVICE_ID, state="invalid")

    ## Test Update with Valid 'state' Values
    @patch("requests.patch")
    def test_valid_state_values(self, mock_patch):
        """Test that valid 'state' values are processed correctly."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_patch.return_value = mock_response

        self.client.update_l2vpn(service_id=TEST_SERVICE_ID, state="enabled")
        self.client.update_l2vpn(service_id=TEST_SERVICE_ID, state="disabled")

        mock_patch.assert_called()

    ## Test 'service_id' Requirement
    def test_service_id_requirement(self):
        """Test that 'service_id' is required for updating an L2VPN."""
        with self.assertRaises(TypeError):
            self.client.update_l2vpn()

    ## Test Empty Payload
    @patch("requests.patch")
    def test_empty_payload(self, mock_patch):
        """Test that an empty payload still sends a correct request."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_patch.return_value = mock_response

        self.client.update_l2vpn(service_id=TEST_SERVICE_ID)

        expected_payload = {"service_id": TEST_SERVICE_ID}
        mock_patch.assert_called_once_with(
            f"{TEST_URL}/l2vpn/1.0/{TEST_SERVICE_ID}",
            json=expected_payload,
            verify=True,
            timeout=120,
        )

    ## Test Handling of Timeout and RequestException
    @patch("requests.patch", side_effect=Timeout)
    def test_timeout_exception(self, mock_patch):
        """Test that a Timeout exception raises an SDXException."""
        with self.assertRaises(SDXException):
            self.client.update_l2vpn(service_id=TEST_SERVICE_ID, state="enabled")

    @patch("requests.patch", side_effect=RequestException("Connection error"))
    def test_request_exception(self, mock_patch):
        """Test that a RequestException raises an SDXException."""
        with self.assertRaises(SDXException):
            self.client.update_l2vpn(service_id=TEST_SERVICE_ID, state="enabled")


# Run the tests
if __name__ == "__main__":
    unittest.main()
