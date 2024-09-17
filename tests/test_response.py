import unittest
from sdxlib.sdx_response import SDXResponse
from test_config import *

class SDXResponseTest(unittest.TestCase):

    def test_response_initialization_with_valid_json(self):
        response_json = {
            "service_id": TEST_SERVICE_ID,
            "ownership": "user@example.com",
            "creation_date": "20240522T00:00:00Z",
            "archived_date": "0",
            "status": "up",
            "state": "enabled",
            "counters_location": "https://my.aw-sdx.net/l2vpn/7cdf23e8978c",
            "last_modified": "0",
            "current_path": ["urn:sdx:link:tenet.ac.za:LinkToSAX",    
                 "urn:sdx:link:tenet.ac.za:LinkToAmpath",  
                 "urn:sdx:link:ampath.net:LinkToSAX"],
            "oxp_service_ids": {
                    "AmLight.net": ["c73da8e1"], 
                    "TENET.ac.za": ["5d034620"], 
                    "SAX.br": ["7cdf23e8978c"]
            }
        }
        response = SDXResponse(response_json)
        self.assertEqual(response.service_id, TEST_SERVICE_ID)
        self.assertEqual(response.ownership, "user@example.com")
        self.assertEqual(response.creation_date, "20240522T00:00:00Z")
        self.assertEqual(response.archived_date, "0")
        self.assertEqual(response.status, "up")
        self.assertEqual(response.state, "enabled")
        self.assertEqual(response.counters_location, "https://my.aw-sdx.net/l2vpn/7cdf23e8978c")
        self.assertEqual(response.last_modified, "0")
        self.assertEqual(response.current_path, ["urn:sdx:link:tenet.ac.za:LinkToSAX",    
                 "urn:sdx:link:tenet.ac.za:LinkToAmpath",  
                 "urn:sdx:link:ampath.net:LinkToSAX"]
                 )
        self.assertEqual(response.oxp_service_ids, {
                    "AmLight.net": ["c73da8e1"], 
                    "TENET.ac.za": ["5d034620"], 
                    "SAX.br": ["7cdf23e8978c"]
            }
        )

    def test_response_initialization_with_missing_attributes(self):
        response_json = {
            "service_id": "12345678-abcd-efgh-ijkl-mnopqrstuvwxyz"
        }
        response = SDXResponse(response_json)
        self.assertIsNone(response.archived_date)
        self.assertIsNone(response.counters_location)

    def test_response_initialization_with_invalid_json(self):
        response_json = "invalid_json"
        with self.assertRaises(TypeError):
            SDXResponse(response_json)

