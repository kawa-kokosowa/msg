# TODO: use session connectio npooling for requests
"""msgboard: simple restful text message board.

Usage:
    msgboard.py
    msgboard.py init_db
    msgboard.py -h | --help

Options:
    -h --help    Show this screen.

"""

from gevent.pywsgi import WSGIServer
from flask_limiter import Limiter
from flask_httpauth import HTTPBasicAuth

from . import models
from . import config

import os
import json
import docopt
import gevent
import flask_restful
import flask
import requests
import sqlalchemy
import flask_sqlalchemy

app = flask.Flask(__name__)

config_path = os.path.dirname(os.path.abspath(__file__))
app.config.from_pyfile(os.path.join(config_path, "config.py"))
api = flask_restful.Api(app, catch_all_404s=True)
limiter = Limiter(app)
db = flask_sqlalchemy.SQLAlchemy(app)
auth = HTTPBasicAuth()


class User(flask_restful.Resource):
    """API tools for managing, creating, etc.,
    users in the system.

    """

    def get(self, user_id=None, username=None):
        """Get a specific user's info.

        Should elaborate. Be able to specify username
        or by user_id.

        """

        if user_id:
            user = db.session.query(models.User).get(user_id)

            if user is None:
                message = "No user matching ID: %s" % user_id
                flask_restful.abort(404, message=message)

        elif username:
            user = (db.session.query(models.User)
                    .filter(models.User.username == username).first())

            if user is None:
                message = "No user matching username: %s" % username
                flask_restful.abort(404, message=message)

        else:
            message = "Must specify user_id or username."
            flask_restful.abort(400, message=message)

        return user.to_dict()

    def post(self):
        """Create a new user.

        """

        json_data = flask.request.get_json(force=True)
        username = json_data['username']
        password = json_data['password']
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

    def get(self):
        json_data = flask.request.get_json(force=True)
        query = db.session.query(models.Message)

        if 'limit' in json_data:
            limit = int(json_data['limit'])
            assert limit <= config.POSTS_GET_LIMIT_MAX
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

    @auth.login_required
    def put(self, message_id):
        """Edit an existing message.

        """

        json_data = flask.request.get_json(force=True)
        try:
            text = json_data['text']
        except:
            raise Exception(json_data)
        result = db.session.query(models.Message).get(message_id)

        if result.user.username == auth.username():
            result.text = text
            db.session.commit()
            return self.get(message_id)

        else:
            message = "You are not this message's author."
            flask_restful.abort(400, message=message)

    @auth.login_required
    def post(self):
        """Create a new message.

        """

        json_data = flask.request.get_json(force=True)
        text = json_data['text']
        user_id = (db.session.query(models.User)
                   .filter(models.User.username == auth.username())
                   .first().id)
        new_message = models.Message(user_id, text)
        db.session.add(new_message)
        db.session.commit()
        return self.get(new_message.id)

    @auth.login_required
    def delete(self, message_id):
        """Delete a specific message.

        """

        result = db.session.query(models.Message).get(message_id)

        if result.user.username == auth.username():
            db.session.delete(result)
            db.session.commit()
            # TODO: return SOMETHING!
        else:
            message = "You're not the author of message %d" % message_id
            flask_restful.abort(400, message=message)

    def get(self, message_id):
        """Get a specific post.

        """

        result = db.session.query(models.Message).get(message_id)

        if result:
            return result.to_dict()
        else:
            message = "Cannot find message by id: %s" % message_id
            flask_restful.abort(404, message=message)


class Stream(flask_restful.Resource):
    """A live event stream (especiall for JavaScript
    EventSource) for new messages.

    """

    def get(self):
        """Get events from the stream.

        """

        return flask.Response(self.event(), mimetype="text/event-stream")

    def event(self):
        """The actual event magic.

        """

        with app.app_context():

            try:
                result = (db.session.query(models.Message).limit(1)
                          .order_by(flask_sqlalchemy
                                    .desc(models.Message.created)))
                latest_message_id = result.id
            except AttributeError:
                # .id will raise AttributeError if
                # the query doesn't match anything
                latest_message_id = 0

        while True:

            with app.app_context():
                messages = (db.session.query(models.Message)
                            .filter(models.Message.id > latest_message_id)
                            .order_by(models.Message.id.asc()).all())

            if messages:
                latest_message_id = messages[-1].id
                newer_messages = [message.to_dict() for message in messages]
                yield "data: " + json.dumps(newer_messages) + "\n\n"

            with app.app_context():
                gevent.sleep(app.config['SLEEP_RATE'])


@auth.verify_password
def get_password(username, password):
    result = (db.session.query(models.User)
              .filter(models.User.username == username).first())

    if result is None:
        return False
    else:
        return result.check_password(password)


def init_db():
    """For use on command line for setting up
    the database.
    """

    models.Base.metadata.drop_all(bind=db.engine)
    models.Base.metadata.create_all(bind=db.engine)
    db.session.commit()


api.add_resource(Message, '/message', '/message/<int:message_id>')
api.add_resource(Messages, '/messages', '/messages/<int:page>')
api.add_resource(Stream, '/stream')
api.add_resource(User, '/user', '/user/<int:user_id>', '/user/<username>')


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)

    if arguments['init_db']:
        init_db()

    WSGIServer(('', 5000), app).serve_forever()
