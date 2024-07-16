from client import SDXClient

class SDXException(Exception):
    """Custom exception class for SDXClient API errors.

    Attributes:
        status_code (int): HTTP status code associated with the error.
        method_messages (dict, optional): Dictionary mapping error codes to
            specific messages for a particular method (e.g., create_l2vpn,
            update_l2vpn).
    """

    def __init__(
        self, status_code, method_messages=None
    ):
        """Initializes an SDXException with status code and message.

        Args:
            status_code (int): HTTP status code.
            method_messages (dict, optional): Dictionary mapping error codes to
                specific messages for a particular method.

        Raises:
            None
        """
        super().__init__(f"Error {status_code}")
        self.status_code = status_code
        self.method_messages = method_messages