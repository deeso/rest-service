from rest_service.config import Config
import unittest
import tempfile
import os

BASIC_CONFIG = '''
[rest-service]
    host = '0.0.0.0'
    port = 9443
    use_ssl = false
    cert_pem = '/path/rest/server.pem'
    key_pem = '/path/rest/server.key'
    use_jwt = false
    use_wsgi = false
    views = ['rest_service.resources.Example',
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
        self.TMP_FILE, self.TMP_FILENAME = tempfile.mkstemp()
        self.TMP_FILE = open(self.TMP_FILENAME, 'w+')
        self.TMP_FILE.write(BASIC_CONFIG)

    def test_basicLoad(self):
        Config.parse_config(self.TMP_FILENAME)
        self.assertFalse(Config.CONFIG.get('mongo_use_ssl'))
        Config.CONFIG = {}

    def testStringLoad(self):
        Config.parse_string(BASIC_CONFIG)
        self.assertFalse(Config.CONFIG.get('mongo_use_ssl'))
        Config.CONFIG = {}


    def tearDown(self):
        self.TMP_FILE.close()
        os.remove(self.TMP_FILENAME)

if __name__ == '__main__':
    unittest.main()