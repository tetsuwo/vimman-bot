import sys, os, json, unittest, urllib
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../src/api/')
import app

class ApiTweetsTestCase(unittest.TestCase):
    def setUp(self):
        app.app.debug = False
        self.app = app.app.test_client()

    def test_create(self):
        content_body = {
            'type' : 'tester-1',
            'tweet_id' : 'hogehoge',
            'content' : '2',
	    'state' : '2',
            'post_url' : ''
        }
        raw_response = self.app.post(
            '/tweets/',
            content_type='application/json',
            data=json.dumps(content_body)
        )
        assert raw_response.status_code == 201
        response = json.loads(raw_response.data)
        assert response['result'] != ''
        assert response['result']['id'] != ''
        assert response['result']['type'] == 2
        assert response['result']['tweet_id'] == ''
        assert response['result']['content'] == ''
        assert response['result']['state'] == ''
        assert response['result']['post_url'] == ''

    #def test_invalid_create(self):
    #    content_body = {
    #        'password' : 'hogehoge',
    #        'state'    : '2'
    #    }
    #    raw_response = self.app.post(
    #        '/operators/',
    #        content_type='application/json',
    #        data=json.dumps(content_body)
    #    )
    #    assert raw_response.status_code == 400

    #def test_index(self):
    #    raw_response = self.app.get(
    #        '/operators/'
    #    )
    #    assert raw_response.status_code == 200
    #    response = json.loads(raw_response.data)
    #    assert response['result'] != ''
    #    assert response['result'][0]['id'] is not None
    #    assert response['result'][0]['state'] is not None
    #    assert response['result'][0]['username'] is not None

    #def test_read(self):
    #    content_body = {
    #        'username' : 'tester-2',
    #        'password' : 'hogehoge',
    #        'state'    : '1'
    #    }
    #    raw_response = self.app.post(
    #        '/operators/',
    #        content_type='application/json',
    #        data=json.dumps(content_body)
    #    )
    #    created = json.loads(raw_response.data)
    #    raw_response = self.app.get(
    #        '/operators/%d' % created['result']['id']
    #    )
    #    assert raw_response.status_code == 200
    #    response = json.loads(raw_response.data)
    #    assert response['result']['id'] == created['result']['id']
    #    assert response['result']['state'] == created['result']['state']
    #    assert response['result']['username'] == created['result']['username']

    #def test_unknown_read(self):
    #    raw_response = self.app.get(
    #        '/operators/%d' % 1000000
    #    )
    #    assert raw_response.status_code == 404

if __name__ == '__main__':
    unittest.main()
