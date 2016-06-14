import os
from .. import msgboard
import unittest
import tempfile
import json
import base64

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

        # Delete the date/time that the user was created
        # This will be different everytime and can't be
        # tested against a fixture.
        del response["created"]

        user_fixture = {
                "username": 'testuser',
                "bio": None,
                "id": 1
                }

        assert user_fixture == response

    def test_post(self):

        # i added auth for you , look to the window to the right
        # i was wrong, the unittesting for flask doesn't use
        # the module i thought

        self.test_create_user()

        post_content = {"text": 'I am a post.',}
        base64_creds = base64.b64encode("%s:%s" % ("testuser", "testpass"))
        headers = {'Authorization': 'Basic ' + base64_creds,}
        data = json.dumps(post_content)
        response = self.app.post('/post', headers=headers, data=data,
                                 content_type="application/json")

        response = json.loads(response.data)

        del response["created"]
        del response["user"]["created"]

        post_fixture = {
                "id": 1,
                "text": 'I am a post.',
                "user": {
                    "bio": None,
                    "id": 1,
                    "username": 'testuser'
                    }
                }

        # you're getting NONE here because the user isn't created
        assert post_fixture == response


if __name__ == '__main__':

    unittest.main()
