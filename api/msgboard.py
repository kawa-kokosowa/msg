# TODO: use session connectio npooling for requests
"""msgboard: simple restful text message board.

Usage:
    msgboard.py
    msgboard.py init_db
    msgboard.py -h | --help

Options:
    -h --help    Show this screen.

"""

import json
import docopt
import models
import gevent
import flask_restful
import flask
import config
import requests
import flask_sqlalchemy

from gevent import monkey
from gevent.pywsgi import WSGIServer
from flask_limiter import Limiter
from flask_httpauth import HTTPBasicAuth


monkey.patch_all()  # NOTE: totally cargo culting this one

app = flask.Flask(__name__)
app.config.from_object("config")
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
        else:
            user = (db.session.query(models.User)
                    .filter(models.User.username == username).first())

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
        db.session.commit()
        return self.get(new_user.id)


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
        return [r.to_dict() for r in results]


class Post(flask_restful.Resource):

    # FIXME: require that post user is equal to
    # auth user
    @auth.login_required
    def put(self, post_id):
        """Edit an existing post.

        """

        json_data = flask.request.get_json(force=True)
        text = json_data['text']
        result = db.session.query(models.Post).get(post_id)
        result.text = text
        db.session.commit()
        return self.get(post_id)

    @auth.login_required
    def post(self):
        """Create a new post.

        """

        json_data = flask.request.get_json(force=True)
        text = json_data['text']
        user_id = User().get(username=auth.username())['id']
        new_post = models.Post(user_id, text)
        db.session.add(new_post)
        db.session.commit()
        return self.get(new_post.id)

    # FIXME: require that post user equals auth user
    @auth.login_required
    def delete(self, post_id):
        """Delete a specific post.

        """

        result = db.session.query(models.Post).get(post_id)
        db.session.delete(result)
        db.session.commit()

    def get(self, post_id):
        """Get a specific post.

        """

        result = db.session.query(models.Post).get(post_id)

        if result:
            return result.to_dict()


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
                          .order_by(flask_sqlalchemy.desc(Post.created)))
                latest_post_id = result.id
            except AttributeError:
                # .id will raise AttributeError if the query doesn't match anything
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
              .filter(models.User.username==username).first())
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
