import sys
import os
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../src/api/')
import app

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_get(self):
        print 'testing...'
        response = self.app.get('/questions/')
        print response.status_code
        #assert response.status_code == 200
        #assert response.data == 'Hello, World!'
        print response.data

if __name__ == '__main__':
    unittest.main()
