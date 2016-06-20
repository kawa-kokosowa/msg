"""Test the msgboard API.

"""

import os
import json
import base64
import unittest
import tempfile
import functools

from .. import msgboard


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
        """If the database is empty, a GET request
        to /posts endpoint should return a blank list.

        """

        post_range = {"offset": 0, "limit": 10}
        response = self.get('/posts', data=post_range)
        assert [] == response

    def __getattr__(self, attribute_name):
        """This is so you can call self.post, self.get, self.put,
        self.post, etc. This only happens when there is no such
        attribute of name...

        """

        if attribute_name.lower() in ('post', 'get', 'put', 'delete'):
            specific_call_method = functools.partial(self.call, attribute_name.lower())
            return specific_call_method

        raise AttributeError("%s is not valid method" % attribute_name)

    def call(self, method, *args, **kwargs):
        """Because we're tired of entering content_type and
        translating JSON constantly!

        """

        method = method.lower()

        # we want this no matter what
        kwargs['content_type'] = 'application/json'

        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])

        response = getattr(self.app, method)(*args, **kwargs)
        return json.loads(response.data)

    def test_create_user(self):
        """Create a user by POST'ing the correct
        JSON data to the /user endpoint.

        """

        # Create and send the user data
        user_data = {
                "username": 'testuser',
                "password": 'testpass'
                }
        
        response = self.post('/user', data=user_data)

        # parse the JSON response and remove the created
        # datetime because that's not predictable
        del response["created"]
        # We expect the response will be this.
        user_fixture = {
                        "username": "testuser",
                        "id": 1,
                        "bio": None
                       }
        # test the expected response vs. actual
        assert user_fixture == response

    def test_get_user(self):
        self.test_create_user()
        user_fixture = {
                        "username": 'testuser',
                        "id": 1,
                        "bio": None
                       }
        # First test by using the user_id
        id_response = self.get('/user/1')
        del id_response["created"]
        assert user_fixture == id_response

        # Then test by using the username
        name_response = self.get('/user/testuser')
        del name_response["created"]

        assert user_fixture == name_response


    def test_post(self):
        self.test_create_user()

        post_content = {"text": 'I am a post.',}
        base64_creds = base64.b64encode("%s:%s" % ("testuser", "testpass"))
        headers = {'Authorization': 'Basic ' + base64_creds,}
        response = self.post('/post', headers=headers, data=post_content)

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

    def test_get_post(self):
        self.test_post()
        response = self.get('/post/1')
        del response['created']
        del response['user']['created']

        post_fixture = {
                        "id": 1,
                        "text": 'I am a post.',
                        "user": {
                                 "bio": None,
                                 "id": 1,
                                 "username": 'testuser'
                                }
                       }
        assert post_fixture == response

    def test_edit_post(self):
        self.test_get_post()
        edited_post_fixture = {
                               "id": 1,
                               "text": 'I am an edited post.',
                               "user": {
                                        "bio": None,
                                        "id": 1,
                                        "username": 'testuser'
                                       }
                              }
        edit_content = {"text": 'I am an edited post.'}

        b64creds = base64.b64encode("%s:%s" % ("testuser", "testpass"))
        headers = {"Authorization": "Basic " + b64creds}

        response = self.put('/post/1', headers=headers, data=edit_content)

        del response["created"]
        del response["user"]["created"]

        assert edited_post_fixture == response


if __name__ == '__main__':
    unittest.main()
