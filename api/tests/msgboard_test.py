"""Test the msgboard API.

"""

import os
import unittest
import tempfile
import json

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
        response = self.app.get('/posts', data=json.dumps(post_range),
                                content_type="application/json")
        assert [] == json.loads(response.data)

    def test_create_user(self):
        """Create a user by POST'ing the correct
        JSON data to the /user endpoint.

        """

        # Create and send the user data
        user_data = {"username": "testuser",
                      "password": "testpass",
                      "bio": "doopy dops bloop blops",}
        response = self.app.post('/user', data=json.dumps(user_data),
                                 content_type="application/json")

        # parse the JSON response and remove the created
        # datetime because that's not predictable
        response = json.loads(response.data)
        del response["created"]
        # We expect the response will be this.
        user_fixture = {"username": "testuser",
                        "bio": "doopy dops bloop blops",
                        "id": 1,}
        # test the expected response vs. actual
        assert user_fixture == response


if __name__ == '__main__':
    unittest.main()
