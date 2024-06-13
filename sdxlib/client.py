import requests

class SDXClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_l2vpn(self, name, endpoints):
        url = f"{self.base_url}/l2vpn"
        payload = {
            "name": name,
            "endpoints": endpoints
        }
        response = requests.post(url, json=payload)

        if response.ok:
            return response.json()
        else:
            raise SDXException(status_code=response.status_code, message=response.text)
    
class SDXException(Exception):
    def __init__(self, status_code, message):
        super().__init__(f"Error {status_code}: {message}")
        self.status_code = status_code
        self.message = message
