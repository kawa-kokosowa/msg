"""msgboard: simple restful text message board.

Usage:
    msgboard.py
    msgboard.py init_db
    msgboard.py -h | --help

Options:
    -h --help    Show this screen.

"""

import docopt
import models
import flask_restful
import flask
import config

from flask_limiter import Limiter
from flask_sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.config.from_object("config")
api = flask_restful.Api(app)
db = SQLAlchemy(app)


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


def init_db():
    """For use on command line for setting up
    the database.
    """

    models.Base.metadata.drop_all(bind=db.engine)
    models.Base.metadata.create_all(bind=db.engine)
    db.session.commit()


api.add_resource(Post, '/post', '/post/<int:post_id>')
api.add_resource(Posts, '/posts', '/posts/<int:page>')


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)

    if arguments['init_db']:
        init_db()

    app.run(debug=True)
