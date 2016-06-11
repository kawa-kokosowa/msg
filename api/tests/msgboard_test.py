import os
from .. import msgboard
import unittest
import tempfile
import json

class MsgboardTestCase(unittest.TestCase):

    def setUp(self):

        self.db_fd, msgboard.app.config['DATABASE'] = tempfile.mkstemp()
        msgboard.app.config['TESTING'] = True
        self.app = msgboard.app.test_client()
        msgboard.init_db()

    def tearDown(self):
        
        os.close(self.db_fd)
        os.unlink(msgboard.app.config['DATABASE'])

    def test_empty_db(self):

        post_range = {
                "offset": 0,
                "limit": 10
                }

        data = json.dumps(post_range)
        response = self.app.get('/posts', data=data,
                                content_type="application/json")

        assert [] == json.loads(response.data)

    def test_create_user(self):

        user_creds = {
                "username": "testuser",
                "password": "testpass"
                }

        data = json.dumps(user_creds)
        response = self.app.post('/user', data=data,
                                 content_type="application/json")

        response = json.loads(response.data)

        del response["created"]

        user_fixture = {
                "username": 'testuser',
                "bio": None,
                "id": 1
                }

        assert user_fixture == response

if __name__ == '__main__':

    unittest.main()
