import re
import requests

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
        self.scheduling = {}
        self.qos_metrics = {}

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
            raise ValueError("Name must be a non-empty string with maximum 50 characters.")
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
        if value is not None and len(value) > 255:
            raise ValueError("Description attribute must be less than 256 characters.")
        self._description = value

    @property
    def notifications(self):
        return self._notifications

    @notifications.setter
    def notifications(self, value):
        self._notifications = self._validate_notifications(value)

    @staticmethod
    def is_valid_email(email):
        email_regex = (
            r"^\S+@\S+$"
        )
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
            if has_special_vlan and (len(vlans) > 1 or has_single_vlan or has_vlan_range):
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
                raise ValueError(f"Invalid VLAN value: '{vlan_value}'. Must be between 1 and 4095.")
        elif ":" in vlan_value:
            vlan_range = vlan_value.split(":")
            if len(vlan_range) != 2:
                raise ValueError(f"Invalid VLAN range values: '{vlan_value}'. Must be 'VLAN ID1:VLAN ID2'.")
            try:
                vlan_id1, vlan_id2 = map(int, vlan_range)
                if not (1 <= vlan_id1 < vlan_id2 <= 4095):
                    raise ValueError(f"Invalid VLAN range values: '{vlan_value}'. Must be between 1 and 4095, and VLAN ID1 must be less than VLAN ID2.")
            except ValueError:
                raise ValueError(f"Invalid VLAN range format: '{vlan_value}'. Must be 'VLAN ID1:VLAN ID2'.")
        else:
            raise ValueError(f"Invalid VLAN value: '{vlan_value}'. Must be 'any', 'all', 'untagged', a string representing an integer between 1 and 4095, or a range.")

        return endpoint_dict
    
    # def update_endpoints(self, endpoints):
    #     self.endpoints = endpoints

    def create_l2vpn(self):
        """
        Creates an L2VPN using the provided name and endpoints.

        Returns:
        - dict: JSON response from the API if successful.

        Raises:
        - ValueError: If name or endpoints are not provided
            or do not meet requirements.
        - SDXException: If the API request fails.
        """

        if self.name is None:
            raise ValueError("Name attribute is required.")
        if not self.endpoints:
            raise ValueError("Endpoints attribute is required.")

        url = f"{self.base_url}/l2vpn"

        payload = {
            "name": self.name,
            "endpoints": [
                {"port_id": endpoint["port_id"], "vlan": endpoint["vlan"]}
                for endpoint in self.endpoints
            ],
        }
        response = requests.post(url, json=payload)

        if response.ok:
            return response.json()
        else:
            raise SDXException(status_code=response.status_code, message=response.text)

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

    client = SDXClient(
        base_url="http://example.com", name=client_name, endpoints=client_endpoints
    )

    try:
        response = client.create_l2vpn()
        print(response)
    except ValueError as e:
        print(f"Error: {e}")
    except SDXException as e:
        print(f"SDX Error: {e.status_code} - {e.message}")
