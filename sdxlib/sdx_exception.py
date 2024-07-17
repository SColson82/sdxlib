class SDXException(Exception):
    """Custom exception class for SDXClient API errors.

    Attributes:
        status_code (int): HTTP status code associated with the error.
        method_messages (dict, optional): Dictionary mapping error codes to
            specific messages for a particular method (e.g., create_l2vpn,
            update_l2vpn).
        message (str): General error message describing the exception.
    """

    def __init__(self, status_code=None, method_messages=None, message=None):
        """Initializes an SDXException with status code and message.

        Args:
            status_code (int): HTTP status code.
            method_messages (dict, optional): Dictionary mapping error codes to
                specific messages for a particular method.

        Raises:
            None
        """
        self.status_code = status_code
        self.method_messages = method_messages
        self.message = message or (
            method_messages.get(status_code) if method_messages else ""
        )
        super().__init__(self.message)
