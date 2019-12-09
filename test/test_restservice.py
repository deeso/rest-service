from rest_service.config import Config
from rest_service.service import RestService
import unittest
import time
import os
import requests

BASIC_CONFIG = '''
[rest-service]
    host = '0.0.0.0'
    port = 9448
    use_ssl = false
    cert_pem = '/path/rest/server.pem'
    key_pem = '/path/rest/server.key'
    use_jwt = false
    use_wsgi = false
    views = ['rest_service.resources.ExampleView',
             'rest_service.resources.ExampleAdminView',
             'rest_service.resources.ExampleUserView'  ]

    using_postgres = false
    postgres_host = '1.80.67.2'
    postgres_port = 5432
    postgres_user = 'postres_test'
    postgres_pass = '9C4q&7$ES9X1a1M^gA4369p9C4q&7$ES9X1a1M^gA4369p9C4q&7$ES9X1a1M^gA4369p'
    postgres_use_ssl = false
    postgres_db = 'rest-service'

    using_mongo = false
    mongo_host = '1.80.67.2'
    mongo_port = 5432
    mongo_user = 'postres_test'
    mongo_pass = '9C4q&7$ES9X1a1M^gA4369p9C4q&7$ES9X1a1M^gA4369p9C4q&7$ES9X1a1M^gA4369p'
    mongo_use_ssl = false
    mongo_db = 'rest-service'''

class TestConfigLoad(unittest.TestCase):
    TMP_FILE = None
    TMP_FILENAME = None

    def setUp(self):
        Config.parse_string(BASIC_CONFIG)

    def test_basicLoad(self):
        rs = RestService.from_config()
        self.assertTrue(len(rs.views) == 3)

    def test_basicStartRequest(self):
        rs = RestService.from_config()
        rs.run()
        rsp = requests.get("http://127.0.0.1:9448/example")
        self.assertTrue(rsp.content == b'{"result": "example works"}')
        rs.stop()


if __name__ == '__main__':
    unittest.main()