import sys, os, json, unittest, urllib
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../src/api/')
import app

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        app.app.debug = False
        self.app = app.app.test_client()

    def test_questions_index(self):
        raw_response = self.app.get('/questions/')
        assert raw_response.status_code == 200
        assert raw_response.headers['Content-Type'] == 'application/json'
        response = json.loads(raw_response.data)
        assert response['status_code'] == 200
        #assert len(response['result']) == 0

    def test_questions_create(self):
        content_body = {
            'questions[state]' : '1',
            'questions[content]' : 'ABCDEDG',
            'questions[answer]' : 'hoge'
        }
        raw_response = self.app.post('/questions/', content_type='application/x-www-form-urlencoded; charset=UTF-8', data=content_body)
        raw_response = json.loads(raw_response.data)
        assert raw_response.status_code == 200
        assert raw_response.headers['Content-Type'] == 'application/json'
        response = json.loads(raw_response.data)
        assert response['status_code'] == 200
        #assert len(response['result']) == 0

    def test_informations_index(self):
        raw_response = self.app.get('/informations/')
        print raw_response
        assert raw_response.status_code == 200
        assert raw_response.headers['Content-Type'] == 'application/json'
        response = json.loads(raw_response.data)
        #assert response['status_code'] == 200
        #assert len(response['result']) == 0

    def test_informations_create(self):
        #content_body = 'informations[state]=1&informations[content]=ABCED'
        content_body = {
            'state'   : '1',
            'content' : 'INFORMATION-ABCDEDG'
        }
        #print urllib.urlencode(content_body)
        #print urllib.unquote(urllib.urlencode(content_body))
        #return
        #raw_response = self.app.post(
        #    '/informations/',
        #    content_type='application/x-www-form-urlencoded; charset=UTF-8',
        #    data=urllib.unquote(urllib.urlencode(content_body))
        #)
        raw_response = self.app.post(
            '/informations/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        print raw_response

    def test_tweets_index(self):
        raw_response = self.app.get('/tweets/')
        assert raw_response.status_code == 200
        assert raw_response.headers['Content-Type'] == 'application/json'
        response = json.loads(raw_response.data)
        print response
        #assert response['status_code'] == 200
        #assert len(response['result']) == 0

    def test_responses_index(self):
        raw_response = self.app.get('/responses/')
        assert raw_response.status_code == 200
        assert raw_response.headers['Content-Type'] == 'application/json'
        response = json.loads(raw_response.data)
        assert response['status_code'] == 200
        #assert len(response['result']) == 0

if __name__ == '__main__':
    unittest.main()
