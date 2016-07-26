"""msgboard: simple REST msg library.

Usage:
    msgboard.py init_db
    msgboard.py -h | --help

Options:
    -h --help    Show this screen.

"""

from flask_httpauth import HTTPBasicAuth

#import models
#import config
from . import models
from . import config

import flask_limiter
from flask_sse import sse

import os
import json
import docopt
import flask_restful
import flask
import requests
import sqlalchemy
import flask_sqlalchemy

app = flask.Flask(__name__)

config_path = os.path.dirname(os.path.abspath(__file__))
app.config.from_pyfile(os.path.join(config_path, "config.py"))
app.register_blueprint(sse, url_prefix='/stream')
api = flask_restful.Api(app, catch_all_404s=True)
limiter = flask_limiter.Limiter(
                                app,
                                key_func=(flask_limiter.util.
                                          get_remote_address),
                                global_limits=config.LIMITS_GLOBAL
                               )
db = flask_sqlalchemy.SQLAlchemy(app)
auth = HTTPBasicAuth()


class User(flask_restful.Resource):
    """User account resource; manage users
    in the system.

    """

    @limiter.limit(config.LIMITS_USER_GET)
    def get(self, user_id=None, username=None):
        """Get a specific user's info by user ID
        *or* username.

        This returns a 400 if neither user_id nor
        username was provided. Returns a 404 if
        cannot find a user by the provided user ID
        or username.

        Arguments:
            user_id (int|None): --
            username (str|None): --

        Returns:
            None: If aborted.
            dict: If such a user is found, the return value
                is a dictionary describing the user.

        """

        if user_id is not None:
            user = db.session.query(models.User).get(user_id)

            if user is None:
                message = "No user matching ID: %s" % user_id
                flask_restful.abort(404, message=message)

        elif username is not None:
            user = (db.session.query(models.User)
                    .filter(models.User.username == username).first())

            if user is None:
                message = "No user matching username: %s" % username
                flask_restful.abort(404, message=message)

        else:
            message = "Must specify user_id or username."
            flask_restful.abort(400, message=message)

        return user.to_dict()

    @limiter.limit(config.LIMITS_USER_GET)
    def post(self):
        """Create a new user.

        If a user already exists with the provided
        username, an HTTP 400 is sent.

        Returns:
            dict: If the user was successfully created,
                return a dictionary describing that
                created user.
            None: If aborted.

        """

        json_data = flask.request.get_json(force=True)

        try:
            username = json_data['username']
            password = json_data['password']
        except KeyError:
            message = "Must specify username and password."
            flask_restful.abort(400, message=message)

        bio = json_data.get('bio')
        new_user = models.User(username, password, bio=bio)
        db.session.add(new_user)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            message = "A user already exists with username: %s" % username
            flask_restful.abort(400, message=message)
        else:
            return new_user.to_dict()


class Messages(flask_restful.Resource):
    """Manage more than one message at a time!

    """

    # TODO: Make hard limits on this. Force people
    # to always provide limit and offset (config)
    # and implement abort when both not provided,
    # as well as if the scope is too large.
    @limiter.limit(config.LIMITS_MESSAGES_GET)
    def get(self):
        """Get a range of messages using a "limit"
        and an "offset."

        Returns:
            list: list of dictionaries describing
                messages, if successful.
            None: If aborted.

        """

        json_data = flask.request.get_json(force=True)
        # NOTE: the logic this implies is that if neither
        # limit nor offset is specified, all messages will
        # be returned (not the best behavior imo).
        query = db.session.query(models.Message)

        if 'limit' in json_data:
            limit = int(json_data['limit'])
            assert limit <= config.LIMITS_MESSAGES_GET_LIMIT
            query = query.limit(limit)

        if 'offset' in json_data:
            offset = int(json_data['offset'])
            query = query.offset(offset)

        results = query.all()

        if results is None:
            message = "No messages found at offset %s limit %s"
            flask_restful.abort(404, message=message)
        else:
            return [r.to_dict() for r in results]


class Message(flask_restful.Resource):
    """Message resource; manage a single message!

    """

    @auth.login_required
    @limiter.limit(config.LIMITS_MESSAGE_PUT)
    def put(self, message_id):
        """Edit an existing message.

        Argument:
            message_id (int): --

        """

        json_data = flask.request.get_json(force=True)
        text = json_data['text']
        result = db.session.query(models.Message).get(message_id)

        if result.user.username == auth.username():
            result.text = text
            db.session.commit()
            return self.get(message_id)

        else:
            message = "You are not this message's author."
            flask_restful.abort(400, message=message)

    @auth.login_required
    @limiter.limit(config.LIMITS_MESSAGE_POST)
    def post(self):
        """Create a new message.

        """

        json_data = flask.request.get_json(force=True)

        try:
            text = json_data['text']
        except KeyError:
            flask_restful.abort(400, message="You must specify text field.")

        user_id = (db.session.query(models.User)
                   .filter(models.User.username == auth.username())
                   .first().id)
        new_message = models.Message(user_id, text)
        db.session.add(new_message)
        db.session.commit()
        new_message_from_db = self.get(new_message.id)
        sse.publish(new_message_from_db, type='message')
        return new_message_from_db

    @auth.login_required
    @limiter.limit(config.LIMITS_MESSAGE_DELETE)
    def delete(self, message_id):
        """Delete a specific message.

        Argument:
            message_id (int): --

        """

        result = db.session.query(models.Message).get(message_id)

        if result is None:
            flask_restful.abort(404, message="No post by id %d" % message_id)

        if result.user.username == auth.username():
            db.session.delete(result)
            db.session.commit()
            return {}
        else:
            message = "You're not the author of message %d" % message_id
            flask_restful.abort(401, message=message)

    @limiter.limit(config.LIMITS_MESSAGE_GET)
    def get(self, message_id):
        """Get a specific post.

        """

        result = db.session.query(models.Message).get(message_id)

        if result:
            return result.to_dict()
        else:
            message = "Cannot find message by id: %s" % message_id
            flask_restful.abort(404, message=message)


@auth.error_handler
def auth_error():
    flask_restful.abort(401, message="Unathorized")


@auth.verify_password
def get_password(username, password):
    """For HTTPBasicAuth; this simply gets the
    corresponding user, then return the result
    of checking that password.

    Arguments:
        username (str):
        password (str):

    See Also:
        flask_httpauth

    Returns:
        bool: True if the password is correct for the supplied
            username, False otherwise.

    """

    result = (db.session.query(models.User)
              .filter(models.User.username == username).first())

    if result is None:
        return False
    else:
        return result.check_password(password)


def init_db():
    models.Base.metadata.drop_all(bind=db.engine)
    models.Base.metadata.create_all(bind=db.engine)
    db.session.commit()


api.add_resource(Message, '/message', '/message/<int:message_id>')
api.add_resource(Messages, '/messages', '/messages/<int:page>')
api.add_resource(User, '/user', '/user/<int:user_id>', '/user/<username>')


if config.SQLALCHEMY_DATABASE_URI == "sqlite:///:memory:":
    init_db()

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)

    if arguments['--init_db']:
        init_db()
