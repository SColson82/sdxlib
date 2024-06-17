import requests

"""
sdxlib

A Python client library for interacting with the AtlanticWave-SDX L2VPN API.

"""

class SDXClient:
    def __init__(self, base_url):
        """
        Initializes an instance of SDXClient.

        Args:
        - base_url (str): The base URL of the SDX API.

        Attributes:
        - base_url (str): The base URL of the SDX API.
        - _name (str of None): Private attribute for storing the name of the L2VPN.
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
        - str or None: The name of the L2VPN.

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
        - ValueError: If the provided name exceeds 50 characters.
        """
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if len(value) > 50:
            raise ValueError("Name must be 50 characters or fewer.")
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
        - TypeError: If the provided endpoints are not a list.
        - ValueError: If the endpoints list has less than 2 entries or contains non-dictionary elements.
        """
        if not isinstance(value, list):
            raise TypeError("Endpoints must be a list.")
        
        if not all(isinstance(item, dict) for item in value):
            raise TypeError("Endpoints must be a list of dictionaries.")
        
        if len(value) < 2:
            raise ValueError("Endpoints must contain at least 2 entries.")
        
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
            raise ValueError("Name is required.")
        if not self.endpoints:
            raise ValueError("Endpoints must not be empty.")
        
        url = f"{self.base_url}/l2vpn"

        payload = {
            "name": self.name,
            "endpoints": [{"port_id": endpoint["port_id"], "vlan": endpoint["vlan"]} for endpoint in self.endpoints]
        }
        response = requests.post(url, json=payload)

        if response.ok:
            return response.json()
        else:
            raise SDXException(status_code=response.status_code, message=response.text)
    
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

if __name__=="__main__":
    # Example usage
    client = SDXClient(base_url="http://example.com")
    client.name = "Test L2VPN"
    client.endpoints = [
        {"port_id": "urn:sdx:port:test:1", "vlan": "100"},
        {"port_id": "urn:sdx:port:test:1", "vlan": "200"}
    ]

    try:
        response = client.create_l2vpn()
        print(response)
    except ValueError as e:
        print(f"Error: {e}")
    except SDXException as e:
        print(f"SDX Error: {e.status_code} - {e.message}")