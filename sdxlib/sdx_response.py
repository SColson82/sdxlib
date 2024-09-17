from typing import Dict, List, Optional

class SDXResponse:
    """
    Class representing a response object from the L2VPN creation API.

    Attributes:
        service_id (str): The service Universally Unique Identifier (UUID).
        ownership (str): The authenticated user or token that submitted the request.
        creation_date (str): The service creation time in ISO8601 format.
        archived_date (str): The datetime of the archive request (initially 0).
        status (str): The current operational status of the L2VPN (up, down, error, under provisioning, maintenance).
        state (str): The current administrative state of the L2VPN (enabled, disabled).
        counters_location (str): The link to the Grafana page with counters.
        last_modified (str): The datetime of the last modification (initially 0).
        current_path (str): The URI of the interdomain links in the path as a list.
        oxp_service_ids (Optional[List[Dict[str, str]]]): A list of dictionaries containing OXP service IDs.
    """

    def __init__(self, response_json: dict):
        """
        Initializes the L2VPNResponse object from a JSON response dictionary.

        Args:
            response_json (dict): The JSON response dictionary from the L2VPN creation API.
        """
        if not isinstance(response_json, dict):
            raise TypeError("Expected a dictionary response_json.")
        
        self.service_id: str = response_json.get("service_id")
        self.ownership: str = response_json.get("ownership")
        self.creation_date: str = response_json.get("creation_date")
        self.archived_date: str = response_json.get("archived_date")
        self.status: str = response_json.get("status")
        self.state: str = response_json.get("state")
        self.counters_location: str = response_json.get("counters_location")
        self.last_modified: str = response_json.get("last_modified")
        self.current_path: List[str] = response_json.get("current_path")
        self.oxp_service_ids: List[Dict[str, str]] = response_json.get("oxp_service_ids")

    def __str__(self) -> str:
        """
        Returns a string representation of the L2VPNResponse object.
        """
        return f"""L2VPN Response:
        service_id: {self.service_id}
        ownership: {self.ownership}
        creation_date: {self.creation_date}
        archived_date: {self.archived_date}
        status: {self.status}
        state: {self.state}
        counters_location: {self.counters_location}
        last_modified: {self.last_modified}
        current_path: {self.current_path}
        oxp_service_ids: {self.oxp_service_ids}"""
