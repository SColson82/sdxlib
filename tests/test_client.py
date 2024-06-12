import unittest
from unittest.mock import patch
from sdxlib.client import SDXClient, SDXException

'''
Unit tests for the sdxlib library

Run from the SDXLIB parent directory Using: 
    python -m unittest discover tests
'''

class TestSDXClient(unittest.TestCase):

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_success(self, mock_post):
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {"status": "Accepted"}

        client = SDXClient(base_url="http://example.com")
        
        response = client.create_l2vpn(
            name=" Test L2VPN",
            endpoints=[{"interface_uri": "urn:sdx:port:test:1", "vlan": "100"}]
        )

        self.assertEqual(response, {"status": "Accepted"})

    @patch('sdxlib.client.requests.post')
    def test_create_l2vpn_failure(self, mock_post):
        mock_post.return_value.ok = False
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = "Bad Request"

        client = SDXClient(base_url="http://example.com")

        with self.assertRaises(SDXException) as context:
            client.create_l2vpn(
                name="Test L2VPN",
                endpoints=[{"interface_uri": "urn:sdx:port:test:1", 
                "vlan": "100"}]
            )
        self.assertEqual(context.exception.status_code, )
        self.assertEqual(context.exception.message, "Bad Request")

if __name__=="__main__":
    unittest.main()