import logging
import re
import requests
from typing import Optional, Dict
from collections import namedtuple
from requests.exceptions import RequestException, HTTPError, Timeout

"""
sdxlib

A Python client library for interacting with the AtlanticWave-SDX L2VPN API.
"""


class SDXClient:
    """
    A client class for managing interactions
        with the AtlanticWave-SDX L2VPN API.

    Attributes:
    - base_url (str): The base URL of the SDX API.
    - _name (str): Private attribute for storing the name of the L2VPN.
    - _endpoints (list): Private attribute for storing the list of endpoints.

    Raises:
    - ValueError: If provided parameters do not meet requirements.
    - SDXException: If an API request fails.
    """

    PORT_ID_PATTERN = (
        r"^urn:sdx:port:[a-zA-Z0-9.,-_\/]+:[a-zA-Z0-9.,-_\/]+:[a-zA-Z0-9.,-_\/]+$"
    )

    VERSION = "1.0.0"

    def __init__(
        self,
        base_url,
        name,
        endpoints,
        description=None,
        notifications=None,
        scheduling=None,
        qos_metrics=None,
    ):
        """
        Initializes an instance of SDXClient.

        Args:
        - base_url (str): The base URL of the SDX API.
        - name (str): The name of the SDX client.
        - endpoints (lsit): List of endpoints associated with the client.
        - description (str, optional): Description of
            the client (default: None).
        - notifications (list, optional): List of
            notification settings (default: None).
        - scheduling (dict, optional): Scheduling
            configuration (default: None).
        - qos_metrics (dict, optional): Quality
            of service metrics (default: None).
        """
        self.base_url = base_url
        self.name = name
        self.endpoints = self._validate_endpoints(endpoints)
        self.description = description
        self.notifications = self._validate_notifications(notifications)
        self.scheduling = scheduling
        self._validate_scheduling(scheduling)
        self.qos_metrics = qos_metrics

    @property
    def name(self):
        """
        Getter method for retrieving the name of the L2VPN.

        Returns:
        - str: The name of the L2VPN.

        Raises:
        - None
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Setter method for setting the name of the L2VPN.

        Args:
        - value (str): The name to be set for the L2VPN.

        Raises:
        - TypeError: If the provided name is not a string.
        - ValueError: If the provided name exceeds
            50 characters or is an empty string.
        """
        if not isinstance(value, str) or not value or len(value) > 50:
            raise ValueError(
                "Name must be a non-empty string with maximum 50 characters."
            )
        self._name = value

    @property
    def endpoints(self):
        """
        Getter method for retrieving the list of endpoints.

        Returns:
        - list: The list of endpoints.

        Raises:
        - None
        """
        return self.__endpoints

    @endpoints.setter
    def endpoints(self, value):
        """
        Setter method for setting the list of endpoints.

        Args:
        - value (list): The list of endpoints to be set.

        Raises:
        - TypeError:
            - If the provided endpoints are not a list.
            - If the endpoints list contains non-dictionary elements.
            - If the VLAN value is not a string.
        - ValueError:
            - If the endpoints list has less than 2 entries.
            - If any endpoint dictionary does not
                contain a non-empty 'port_id' key.
            - If the port_id value does not follow
                the format: 'urn:sdx:port:<oxp_url>:<node_name>:<port_name>'
            - If any endpoint dictionary does not
                contain a non-empty 'vlan' key.
            - If any vlan value is other than an integer
                string, a valid range format, or any of
                    the values 'any', 'all', or 'untagged'.
            - If the vlan value is an integer string that
                is not between 1 and 4095 inclusive.
            - If the vlan value 'all' is used with any
                other value but 'all'.
            - If a range is used for the vlan value with any
                other value but the same range value.
            - If the vlan range value does not follow the
                format 'VLAN ID 1:VLAN ID2' where
                    1 <= VLAN ID1 < VLAN ID2 <= 4095.
        """
        self.__endpoints = self._validate_endpoints(value)

    @property
    def description(self):
        """
        Getter for the description attribute.

        Returns:
        - str: The current description.
        """
        return self._description

    @description.setter
    def description(self, value):
        """
        Setter for the description attribute.

        Args:
        - value (str): The description of the client.

        Raises:
        - ValueError: If the description is longer than 255 characters.
        """
        if value is None or not value:
            self._description = None
        elif value is not None and len(value) > 255:
            raise ValueError("Description attribute must be less than 256 characters.")
        else:
            self._description = value

    @property
    def notifications(self):
        return self._notifications

    @notifications.setter
    def notifications(self, value):
        if value is None or not value:
            self._notifications = None
        else:
            self._notifications = self._validate_notifications(value)

    @property
    def scheduling(self):
        """
        Getter for the scheduling attribute.

        Returns:
            dict: The current scheduling configuration or None if not set.
        """
        return self._scheduling

    @scheduling.setter
    def scheduling(self, value):
        """
        Setter for the scheduling attribute.

        Args:
            value(dict, optional): Scheduling configuration dictionary.

        Raises:
            TypeError: If the provided value is not a dictionary.
            ValueError: If the provided scheduling configuration is invalid.
        """
        if value is None or not value:
            self._scheduling = None
            return
        if value is not None and not isinstance(value, dict):
            raise TypeError("Scheduling attribute must be a dictionary.")

        self._validate_scheduling(value)
        self._scheduling = value

    @property
    def qos_metrics(self):
        return self._qos_metrics

    @qos_metrics.setter
    def qos_metrics(self, value: Optional[Dict[str, Dict[str, int]]]):

        if value is None or not value:
            self._qos_metrics = None
            return

        self._validate_qos_metric(value)
        self._qos_metrics = value

    # Endpoints Methods
    def _validate_endpoints(self, endpoints):
        if not isinstance(endpoints, list):
            raise TypeError("Endpoints must be a list.")
        if len(endpoints) < 2:
            raise ValueError("Endpoints must contain at least 2 entries.")

        vlans = set()
        vlan_ranges = set()
        special_vlans = {"any", "all", "untagged"}
        has_vlan_range = False
        has_single_vlan = False
        has_special_vlan = False
        has_any_untagged = False

        validated_endpoints = []
        for endpoint in endpoints:
            validated_endpoint = self._validate_endpoint_dict(endpoint)
            validated_endpoints.append(validated_endpoint)

            vlan_value = endpoint["vlan"]
            if vlan_value in special_vlans:
                vlans.add(vlan_value)
                if vlan_value in {"any", "untagged"}:
                    has_any_untagged = True
                else:
                    has_special_vlan = True
            elif vlan_value.isdigit():
                has_single_vlan = True
                vlans.add(vlan_value)
            elif ":" in vlan_value:
                vlan_ranges.add(vlan_value)
                has_vlan_range = True

            # Check that if range is used, all vlan
            # values are set to the same range.
            if has_vlan_range and (
                len(vlan_ranges) > 1
                or has_single_vlan
                or has_special_vlan
                or has_any_untagged
            ):
                raise ValueError(
                    "All endpoints must have the same VLAN value if one endpoint is 'all' or a range."
                )

            # Check that if 'all' vlan value is used,
            # every vlan value must be 'all'.
            if has_special_vlan and (
                len(vlans) > 1 or has_single_vlan or has_vlan_range
            ):
                raise ValueError(
                    "All endpoints must have the same VLAN value if one endpoint is 'all' or a range."
                )

        return validated_endpoints

    def _validate_endpoint_dict(self, endpoint_dict):
        if not isinstance(endpoint_dict, dict):
            raise TypeError("Endpoints must be a list of dictionaries.")

        # Validate 'port_id'
        if "port_id" not in endpoint_dict or not endpoint_dict["port_id"]:
            raise ValueError("Each endpoint must contain a non-empty 'port_id' key.")
        if not re.match(self.PORT_ID_PATTERN, endpoint_dict["port_id"]):
            raise ValueError(f"Invalid port_id format: {endpoint_dict['port_id']}")

        # Validate 'vlan'
        if "vlan" not in endpoint_dict or not endpoint_dict["vlan"]:
            raise ValueError("Each endpoint must contain a non-empty 'vlan' key.")
        vlan_value = endpoint_dict["vlan"]

        if not isinstance(vlan_value, str):
            raise TypeError("VLAN must be a string.")

        valid_vlans = {"any", "all", "untagged"}

        if vlan_value in valid_vlans:
            pass  # Valid special VLAN value
        elif vlan_value.isdigit():
            vlan_int = int(vlan_value)
            if not (1 <= vlan_int <= 4095):
                raise ValueError(
                    f"Invalid VLAN value: '{vlan_value}'. Must be between 1 and 4095."
                )
        elif ":" in vlan_value:
            vlan_range = vlan_value.split(":")
            if len(vlan_range) != 2:
                raise ValueError(
                    f"Invalid VLAN range values: '{vlan_value}'. Must be 'VLAN ID1:VLAN ID2'."
                )
            try:
                vlan_id1, vlan_id2 = map(int, vlan_range)
                if not (1 <= vlan_id1 < vlan_id2 <= 4095):
                    raise ValueError(
                        f"Invalid VLAN range values: '{vlan_value}'. Must be between 1 and 4095, and VLAN ID1 must be less than VLAN ID2."
                    )
            except ValueError:
                raise ValueError(
                    f"Invalid VLAN range format: '{vlan_value}'. Must be 'VLAN ID1:VLAN ID2'."
                )
        else:
            raise ValueError(
                f"Invalid VLAN value: '{vlan_value}'. Must be 'any', 'all', 'untagged', a string representing an integer between 1 and 4095, or a range."
            )

        return endpoint_dict

    # def update_endpoints(self, endpoints):
    #     self.endpoints = endpoints

    # Notifications Methods
    @staticmethod
    def is_valid_email(email):
        email_regex = r"^\S+@\S+$"
        return re.match(email_regex, email) is not None

    def _validate_notifications(self, notifications):
        if notifications is None:
            return None
        if not isinstance(notifications, list):
            raise ValueError("Notifications must be provided as a list.")
        if len(notifications) > 10:
            raise ValueError("Notifications can contain at most 10 email addresses.")
        if any(
            not isinstance(n, dict)
            or "email" not in n
            or not self.is_valid_email(n["email"])
            for n in notifications
        ):
            raise ValueError("Invalid notification format or email address.")
        return notifications

    # Methods for Scheduling Attribute
    def _validate_scheduling(self, scheduling):
        """
        Validates the provided scheduling configuration dictionary.

        Args:
            scheduling (dict): The scheduling configuration to validate.

        Raises:
            ValueError: If the scheduling configuration is invalid.
        """
        if scheduling:
            if "start_time" not in scheduling and "end_time" not in scheduling:
                return  # Immediate provisioning
            if "start_time" in scheduling and not self._is_valid_iso8601(
                scheduling["start_time"]
            ):
                raise ValueError(
                    "Invalid 'start_time' format. Use ISO8601 format (YYYY-MM-DDTHH:mm:SSZ)."
                )
            if "end_time" in scheduling and not self._is_valid_iso8601(
                scheduling["end_time"]
            ):
                raise ValueError(
                    "Invalid 'end_time' format. Use ISO8601 format (YYYY-MM-DDTHH:mm:SSZ)."
                )
            if "start_time" in scheduling and "end_time" in scheduling:
                if scheduling["end_time"] <= scheduling["start_time"]:
                    raise ValueError("End time must be after start time.")

    def _is_valid_iso8601(self, timestamp):
        """
        Checks if the provided string is a valid ISO8601 formatted timestamp.

        ARgs:
            timestamp(str): The timestamp string to validate.

        Returns:
            bool: True if the format is valid, False otherwise.
        """
        timestamp_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
        return bool(re.match(timestamp_pattern, timestamp))

    # Methods for Qos_metric Attribute
    def _validate_qos_metric(self, qos_metric):
        if qos_metric is None:
            return

        valid_keys = {"min_bw", "max_delay", "max_number_oxps"}
        if not set(qos_metric.keys()) <= valid_keys:
            raise ValueError(
                "Invalid qos_metric keys. Valid keys are: {}".format(
                    ", ".join(valid_keys)
                )
            )

        for key, value_dict in qos_metric.items():
            if not isinstance(value_dict, dict):
                raise TypeError(
                    "qos_metric value for '{}' must be a dictionary.".format(key)
                )
            self._validate_qos_metric_value(key, value_dict)

    def _validate_qos_metric_value(self, key, value_dict):
        if "value" not in value_dict:
            raise ValueError(
                "Missing required key 'value' in qos_metric for '{}'".format(key)
            )
        if not isinstance(value_dict["value"], int):
            raise TypeError("qos value for '{}' must be an integer.".format(key))

        # Specific range checks for each key
        if key == "min_bw":
            if not 0 <= value_dict["value"] <= 100:
                raise ValueError("qos_metric 'min_bw' value must be between 0 and 100.")
        elif key == "max_delay":
            if not 0 <= value_dict["value"] <= 1000:
                raise ValueError(
                    "qos_metric 'max_delay' value must be between 0 and 1000."
                )
        elif key == "max_number_oxps":
            if not 1 <= value_dict["value"] <= 100:
                raise ValueError(
                    "qos_metric 'max_number_oxps' value must be between 1 and 100."
                )

        # 'strict' key validation (default False)
        value_dict.get("strict", False)

    ### Class Methods
    _request_cache = {}
    _logger = logging.getLogger(__name__)

    def create_l2vpn(self):
        """
        Creates an L2VPN using the provided name, endpoints, and
        optional attributes.

        Sends a JSON request body containing the L2VPN configuration to the
        L2VPN API and returns the response.

        Args:
        - name (str, required): Name of the L2VPN
        - endpoints (list, required): Endpoint configuration. 
        - description (str, optional): Description of the L2VPN. Defaults to
        None.
        - notifications (list, optional): List of notification settings.
        Defaults to None.
        -scheduling (dict, optional): Scheduling configuration. Defaults to 
        None.
        qos_metrics (dict, optional): Qualit of service metrics. Defaults to
        None.

        Returns:
        - dict: JSON response from the API containing the service_id and 
        other attributes if successful.
        - None: If the request times out or fails for an unknown reason.

        Raises:
        - SDXException: If the API request fails with a known error code
        and description.
        """

        url = f"{self.base_url}/l2vpn/{self.VERSION}/"

        payload = {
            "name": self.name,
            "endpoints": [
                {"port_id": endpoint["port_id"], "vlan": endpoint["vlan"]}
                for endpoint in self.endpoints
            ],
        }

        # Add optional attributes if provided.
        if self.description:
            payload["description"] = self.description
        if self.notifications:
            payload["notifications"] = self.notifications
        if self.scheduling:
            payload["scheduling"] = self.scheduling
        if self.qos_metrics:
            payload["qos_metrics"] = self.qos_metrics

        # Check cache for existing request with same name and endpoints
        cache_key = (
            self.name,
            tuple(endpoint["port_id"] for endpoint in self.endpoints),
        )
        cached_data = self._request_cache.get(cache_key)

        if cached_data:
            payload, response_json = cached_data
            return response_json
        
        self._logger.info(f"L2VPN creation request sent to {url}.")

        #url = self.base_url + "/l2vpn/{self.VERSION}/"

        print(
            f"L2VPN creation request sent to {url}. It may take several seconds to receive a response."
        )

        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            response_json = response.json()
            cached_data = (payload, response_json)
            self._request_cache[cache_key] = cached_data
            return response_json
        except HTTPError as e:
            error_msg = response.json().get("description", "Unknown error")
            raise SDXException(status_code=e.response.status_code, message=error_msg)
        except RequestException as e:
            self._logger.error(f"An error occurred while creating L2VPN: {e}")
            # print(f"An error occurred while creating L2VPN: {e}")
            return None


    def update_l2vpn(self, service_id, attribute, value):
        """
        Updates an existing L2VPN identified by its service_id.

        Allows modifying any attribute from the request JSON or the state attribute
        from the response JSON.

        Args:
            service_id (str): The UUID of the L2VPN service to update.
            attribute (str): The attribute to modify (from request or response JSON).
            value: The new value to assign to the specified attribute.

        Returns:
            dict: The updated JSON response from the API, including the service_id
                and any modified attributes.
            None: If the request fails due to errors or timeouts.

        Raises:
            ValueError: If an invalid update is attempted (modifying service_id
                or setting state to a non-lowercase 'enabled' or 'disabled')
            SDXException: If the API request fails with a known error code
                and description.
        """

        url = f"{self.base_url}/l2vpn/{self.VERSION}/{service_id}"

        payload = {"service_id": service_id}

        if attribute not in ["service_id", "state"]:
            payload[attribute] = value
        else:
            if attribute == "state" and value.lower() in ("enabled", "disabled"):
                payload[attribute] = value.lower()
            else:
                raise ValueError("Invalid update: Cannot modify service_id. The 'state' attribute can only be changed to 'enabled' or 'disabled'.")

        try:
            response = requests.patch(url, json=payload, verify=True, timeout=120)
            response.raise_for_status() # Raise exception for non-200 status codes
            return response.json()
        except HTTPError as e:
            error_msg = response.json().get("description", "Unknown error")
            raise SDXException(status_code=e.response.status_code, message=error_msg)
        except RequestException as e:
            print (f"An error occurred while updating L2VPN: {e}")
            return None


    def retrieve_l2vpn(self, service_id):
        """
        Retrieves an L2VPN by its service_id.

        Args:
            service_id (str): The UUID of the specific L2VPN to retrieve.

        Returns:
            dict: A dictionary containing the L2VPN information (service_id as key) or None
                if the L2VPN is not found or an error occurs.

        Raises:
            SDXException: If the API request fails with a know error code and description.
        """

        url = f"{self.base_url}/l2vpn/{self.VERSION}/{service_id}"

        try:
            response = requests.get(url, verify=True, timeout=120)
            response.raise_for_status()
            return response.json() if response.content else None
        except HTTPError as e:
            error_msg = response.json().get("description", "Unknown error")
            raise SDXException(stats_code=e.response.status_code, message=error_msg)
        except RequestException as e:
            print(f"An error occurred while retrieving L2VPN: {e}")
            return None

        
    def retrieve_all_l2vpns(self, archived_date="0"):
        """
        Retrieves all L2VPNs based on the archived_date parameter (defaults to active).

        Args:
            archived_date (str, optional): An ISO8601 formatted timestamp string representing
                the archived_date to filter L2VPNs. Defaults to "0" (active).

        Returns:
            dict: A dictionary with L2VPN information (service_id as key) or an empty
                dictionary if no L2VPNs are found.

        Raises:
            SDXException: If the API request fails with a known error code and description.
            ValueError: If an invalid archived_date format is provided.
        """    

        if not self._is_valid_iso8601(archived_date):
            raise ValueError("Invalid archived_date parameter. Must be a valid ISO8601 formatted timestamp.")
        
        url = f"{self.base_url}/l2vpn/{self.VERSION}/{archived_date}"

        try:
            response = requests.get(url, verify=True, timeout=120)
            response.raise_for_status()
            return response.json() if response.content else {}
        except HTTPError as e:
            error_msg = response.json().get("description", "Unknown error")
            raise SDXException(stats_code=e.response.status_code, message=error_msg)
        except RequestException as e:
            print(f"An error occurred while retrieving L2VPN: {e}")
            return None

        
    def delete_l2vpn(self, service_id):
        """
        Deletes an L2VPN based on the provided service_id.

        Args:
            service_id (str): The UUID of the L2VPN to delete.

        Raises: 
            SDXException: If the API request fails with a known error code and desction.
        """
        url = f"{self.base_url}/l2vpn/{self.VERSION}/{service_id}"

        try:
            response = requests.delete(url, verify=True, timeout=120)
            response.raise_for_status()
            #return response.json() if response.content else {}
        except HTTPError as e:
            error_msg = response.json().get("description", "Unknown error")
            raise SDXException(stats_code=e.response.status_code, message=error_msg)
        except RequestException as e:
            print(f"An error occurred while retrieving L2VPN: {e}")
            return SDXException("Error deleteing L2VPN", cause=e)
        
        
        return None

    def __str__(self):
        """
        Returns a string representation of the SDXClient object.

        Returns:
        - str: String representation of the object.
        """
        return f"SDXClient(name={self.name}, endpoints={self.endpoints})"

    def __repr__(self):
        """
        Returns a detailed string representation of teh SDXClient object.

        Returns:
        - str: Detailed string representation of the object.
        """
        return f"SDXClient(base_url={self.base_url}, name={self.name}, endpoints={self.endpoints})"


class SDXException(Exception):
    """
    Custom exception class for SDXClient API errors.

    Attributes:
    - status_code (int): HTTP status code associated with the error.
    - message (str): Error message detailing the exception.

    Raises:
    - None
    """

    def __init__(self, status_code, message):
        """
        Initialized an SDXException with status code and message.

        Args:
        - status_code (int): HTTP status code.
        - message (str): Error message.

        Raises:
        - None
        """
        super().__init__(f"Error {status_code}: {message}")
        self.status_code = status_code
        self.message = message


if __name__ == "__main__":
    # Example usage
    client_name = "Test L2VPN"
    client_endpoints = [
        {
            "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
            "vlan": "100",
        },
        {
            "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
            "vlan": "200",
        },
    ]
    client_description = (
        ""  # This is an example to demonstrate a L2VPN with optional attributes."
    )
    client_notifications = []  # {"email":f"user{i+1}@email.com"} for i in range(10)]
    client_scheduling = {
        # "start_time": "2024-07-04T10:00:00Z",
        # "end_time": "2024-07-05T18:00:00Z"
    }
    client_qos_metrics = {
        # "min_bw": {
        # "value": 5,
        # "strict": False
        # },
        # "max_delay": {
        #     "value": 150,
        #     "strict": True
        # },
        # "max_number_oxps": {
        #     "value": 100,
        #     "strict": True
        # }
    }

    client = SDXClient(
        base_url="http://example.com",
        name=client_name,
        endpoints=client_endpoints,
        description=client_description,
        notifications=client_notifications,
        scheduling=client_scheduling,
        qos_metrics=client_qos_metrics,
    )

    try:
        print(client.name)
        print(client.endpoints)
        print(client.description)
        print(client.notifications)
        print(client.scheduling)
        print(client.qos_metrics)
    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")
    except SDXException as e:
        print(f"SDX Error: {e.status_code} - {e.message}")

    # # Update description
    # response_json = client.update_l2vpn(
    #     "123e4567-e89b-12d3-a456-426655440000", "description", "New description"
    # )

    # # Enable the L2VPN
    # response_json = client.update_l2vpn(
    #     "123e4567-e89b-12d3-a456-426655440000", "state", "enabled"
    # )

    # # Try updating an invalid attribute (service_id)
    # try:
    #     response_json = client.update_l2vpn(
    #         "123e4567-e89b-12d3-a456-426655440000", "service_id", "new-id"
    #     )
    # except ValueError