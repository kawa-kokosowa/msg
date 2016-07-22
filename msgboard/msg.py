# TODO: use session connectio npooling for requests
"""msgboard: simple restful text message board.

Usage:
    msgboard.py
    msgboard.py init_db
    msgboard.py -h | --help

Options:
    -h --help    Show this screen.

"""

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

from gevent import monkey
from gevent.pywsgi import WSGIServer
from flask_limiter import Limiter
from flask_httpauth import HTTPBasicAuth


monkey.patch_all()  # NOTE: totally cargo culting this one

app = flask.Flask(__name__)

config_path = os.path.dirname(os.path.abspath(__file__))
app.config.from_pyfile(os.path.join(config_path, "config.py"))
api = flask_restful.Api(app)
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


class Posts(flask_restful.Resource):

    def get(self):
        json_data = flask.request.get_json(force=True)
        query = db.session.query(models.Post)

        if 'limit' in json_data:
            limit = int(json_data['limit'])
            assert limit <= config.POSTS_GET_LIMIT_MAX
            query = query.limit(limit)

        if 'offset' in json_data:
            offset = int(json_data['offset'])
            query = query.offset(offset)

        results = query.all()

        if results is None:
            message = "No posts found at offset %s limit %s"
            flask_restful.abort(404, message=message)
        else:
            return [r.to_dict() for r in results]


class Post(flask_restful.Resource):

    @auth.login_required
    def put(self, post_id):
        """Edit an existing post.

        """

        json_data = flask.request.get_json(force=True)
        try:
            text = json_data['text']
        except:
            raise Exception(json_data)
        result = db.session.query(models.Post).get(post_id)

        if result.user.username == auth.username():
            result.text = text
            db.session.commit()
            return self.get(post_id)

        else:
            flask_restful.abort(400, message="You are not this post's author.")

    @auth.login_required
    def post(self):
        """Create a new post.

        """

        json_data = flask.request.get_json(force=True)
        text = json_data['text']
        user_id = (db.session.query(models.User)
                   .filter(models.User.username == auth.username())
                   .first().id)
        new_post = models.Post(user_id, text)
        db.session.add(new_post)
        db.session.commit()
        return self.get(new_post.id)

    @auth.login_required
    def delete(self, post_id):
        """Delete a specific post.

        """

        result = db.session.query(models.Post).get(post_id)

        if result.user.username == auth.username():
            db.session.delete(result)
            db.session.commit()
            # TODO: return SOMETHING!
        else:
            message = "You're not the author of post %s" % post_id
            flask_restful.abort(400, message=message)

    def get(self, post_id):
        """Get a specific post.

        """

        result = db.session.query(models.Post).get(post_id)

        if result:
            return result.to_dict()
        else:
            message = "Cannot find post by id: %s" % post_id
            flask_restful.abort(404, message=message)


class Stream(flask_restful.Resource):
    """A live event stream (especiall for JavaScript
    EventSource) for new posts.

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
                result = (db.session.query(models.Post).limit(1)
                          .order_by(flask_sqlalchemy
                                    .desc(models.Post.created)))
                latest_post_id = result.id
            except AttributeError:
                # .id will raise AttributeError if
                # the query doesn't match anything
                latest_post_id = 0

        while True:

            with app.app_context():
                posts = (db.session.query(models.Post)
                         .filter(models.Post.id > latest_post_id)
                         .order_by(models.Post.id.asc()).all())

            if posts:
                latest_post_id = posts[-1].id
                newer_posts = [post.to_dict() for post in posts]
                yield "data: " + json.dumps(newer_posts) + "\n\n"

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


api.add_resource(Post, '/post', '/post/<int:post_id>')
api.add_resource(Posts, '/posts', '/posts/<int:page>')
api.add_resource(Stream, '/stream')
api.add_resource(User, '/user', '/user/<int:user_id>', '/user/<username>')


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)

    if arguments['init_db']:
        init_db()

    WSGIServer(('', 5000), app).serve_forever()
