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

from gevent.pywsgi import WSGIServer
from gevent import monkey
from flask_limiter import Limiter


monkey.patch_all()  # NOTE: totally cargo culting this one

app = flask.Flask(__name__)
app.config.from_object("config")
api = flask_restful.Api(app)
limiter = Limiter(app)
db = flask_sqlalchemy.SQLAlchemy(app)


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

    def put(self, post_id):
        json_data = flask.request.get_json(force=True)
        text = json_data['text']
        result = db.session.query(models.Post).get(post_id)
        result.text = text
        db.session.commit()
        return self.get(post_id)

    def post(self):
        json_data = flask.request.get_json(force=True)
        text = json_data['text']
        new_post = models.Post(text)
        db.session.add(new_post)
        db.session.commit()
        return self.get(new_post.id)

    def delete(self, post_id):
        result = db.session.query(models.Post).get(post_id)
        db.session.delete(result)
        db.session.commit()

    def get(self, post_id):
        result = db.session.query(models.Post).get(post_id)

        if result:
            return result.to_dict()


class Stream(flask_restful.Resource):

    def get(self):
        return flask.Response(self.event(), mimetype="text/event-stream")

    def event(self):

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


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)

    if arguments['init_db']:
        init_db()

    WSGIServer(('', 5000), app).serve_forever()

    app.run(debug=True, threaded=True)
