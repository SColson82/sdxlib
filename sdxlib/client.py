import re
import requests

"""
sdxlib

A Python client library for interacting with the AtlanticWave-SDX L2VPN API.
"""


class SDXClient:

    PORT_ID_PATTERN = (
        r"^urn:sdx:port:[a-zA-Z0-9.,-_\/]+:[a-zA-Z0-9.,-_\/]+:[a-zA-Z0-9.,-_\/]+$"
    )

    def __init__(self, base_url):
        """
        Initializes an instance of SDXClient.

        Args:
        - base_url (str): The base URL of the SDX API.

        Attributes:
        - base_url (str): The base URL of the SDX API.
        - _name (str): Private attribute for storing the name of the L2VPN.
        - _endpoints (list): Private attribute for storing the list of endpoints.

        Raises:
        - None
        """
        self.base_url = base_url
        self._name = None
        self._endpoints = []

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
        - ValueError: If the provided name exceeds 50 characters or is an empty string.
        """
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if len(value) > 50:
            raise ValueError("Name must be 50 characters or fewer.")
        if value == "":
            raise ValueError("Name cannot be an empty string.")
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
        return self._endpoints

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
        - ValueError:
            - If the endpoints list has less than 2 entries.
            - If any endpoint dictionary does not contain a non-empty 'port_id' key.
            - If any endpoint dictionary does not contain a non-empty 'vlan' key.
            - If the port_id value does not follow the format: 'urn:sdx:port:<oxp_url>:<node_name>:<port_name>'
        """
        if not isinstance(value, list):
            raise TypeError("Endpoints must be a list.")

        if not all(isinstance(item, dict) for item in value):
            raise TypeError("Endpoints must be a list of dictionaries.")

        if len(value) < 2:
            raise ValueError("Endpoints must contain at least 2 entries.")

        vlans = set()
        vlan_ranges = set()
        special_vlans = {"any", "all", "untagged"}
        has_vlan_range = False
        has_single_vlan = False
        has_special_vlan = False
        has_any_untagged = False

        for endpoint in value:
            if "port_id" not in endpoint or not endpoint["port_id"]:
                raise ValueError(
                    "Each endpoint must contain a non-empty 'port_id' key."
                )

            if not re.match(self.PORT_ID_PATTERN, endpoint["port_id"]):
                raise ValueError(f"Invalid port_id format: {endpoint['port_id']}")

            if "vlan" not in endpoint or not endpoint["vlan"]:
                raise ValueError("Each endpoint must contain a non-empty 'vlan' key.")

            vlan_value = endpoint["vlan"]

            if not isinstance(vlan_value, str):
                raise TypeError("VLAN must be a string.")

            if vlan_value in special_vlans:
                vlans.add(vlan_value)
                if vlan_value in {"any", "untagged"}:
                    has_any_untagged = True
                else:
                    has_special_vlan = True
            else:
                if vlan_value.isdigit():
                    if not (1 <= int(vlan_value) <= 4095):
                        raise ValueError(
                            f"Invalid VLAN value: '{vlan_value}'. Must be 'any', 'all', 'untagged', a string representing an integer between 1 and 4095, or a range."
                        )
                    has_single_vlan = True
                    vlans.add(vlan_value)
                elif ":" in vlan_value:
                    vlan_range = vlan_value.split(":")
                    if len(vlan_range) == 2:
                        vlan_id1, vlan_id2 = map(int, vlan_range)
                        if not (1 <= vlan_id1 < vlan_id2 <= 4095):
                            raise ValueError(
                                f"Invalid VLAN range values: '{vlan_value}'. Must be between 1 and 4095, and VLAN ID1 must be less than VLAN ID2."
                            )
                        vlan_ranges.add(vlan_value)
                        has_vlan_range = True
                    else:
                        raise ValueError(
                            f"Invalid VLAN range format: '{vlan_value}'. Must be 'VLAN ID1:VLAN ID2'."
                        )
                else:
                    raise ValueError(
                        f"Invalid VLAN value: '{vlan_value}'. Must be 'any', 'all', 'untagged', a string representing an integer between 1 and 4095, or a range."
                    )

        if has_vlan_range and (
            len(vlan_ranges) > 1
            or has_single_vlan
            or has_special_vlan
            or has_any_untagged
        ):
            raise ValueError(
                "All endpoints must have the same VLAN value if one endpoint is 'all' or a range."
            )

        # if "all" in vlans and len(vlans) > 1:
        if has_special_vlan and (len(vlans) > 1 or has_single_vlan or has_vlan_range):
            raise ValueError(
                "All endpoints must have the same VLAN value if one endpoint is 'all' or a range."
            )

        self._endpoints = value

    def create_l2vpn(self):
        """
        Creates an L2VPN using the provided name and endpoints.

        Returns:
        - dict: JSON response from the API if successful.

        Raises:
        - ValueError: If name or endpoints are not provided or do not meet requirements.
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
        return f"SDXClient(name={self.name}, endpoints={self.endpoints})"

    def __repr__(self):
        return f"SDXClient(base_url={self.base_url}, name={self.name}, endpoints={self.endpoints})"


class SDXException(Exception):
    def __init__(self, status_code, message):
        """
        Initializes an SDXException with status code and message.

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
    client = SDXClient(base_url="http://example.com")
    client.name = "Test L2VPN"
    client.endpoints = [
        {
            "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name",
            "vlan": "100",
        },
        {
            "port_id": "urn:sdx:port:test-oxp_url:test-node_name:test-port_name2",
            "vlan": "200",
        },
    ]

    try:
        response = client.create_l2vpn()
        print(response)
    except ValueError as e:
        print(f"Error: {e}")
    except SDXException as e:
        print(f"SDX Error: {e.status_code} - {e.message}")
