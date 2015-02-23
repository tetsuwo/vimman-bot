import sys, os, json, unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../src/api/')
import app

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_questions_get(self):
        raw_response = self.app.get('/questions/')
        assert raw_response.status_code == 200
        assert raw_response.headers['Content-Type'] == 'application/json'
        response = json.loads(raw_response.data)
        assert response['status_code'] == 200
        assert len(response['result']) == 0

if __name__ == '__main__':
    unittest.main()
