import sys, os, json, unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../src/api/')
import app

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_get1(self):
        response = self.app.get('/questions/')
        print response.status_code
        #assert response.status_code == 200
        #assert response.data == 'Hello, World!'
        print response.data
        print "\n\n"

    def test_get2(self):
        response = self.app.get('/questions')
        print response.status_code
        #assert response.status_code == 200
        #assert response.data == 'Hello, World!'
        print response.data
        print "\n\n"

    def test_get3(self):
        response = self.app.get('/api/questions')
        print response.status_code
        #assert response.status_code == 200
        #assert response.data == 'Hello, World!'
        print response.data
        print "\n\n"

    def test_get4(self):
        response = self.app.get('/questions?hoge')
        print response.status_code
        #assert response.status_code == 200
        #assert response.data == 'Hello, World!'
        print response.data
        print "\n\n"

if __name__ == '__main__':
    unittest.main()
