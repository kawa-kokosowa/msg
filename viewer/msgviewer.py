"""msgboard viewer/website, which
interfaces to the API.

"""

import flask
import requests
import json

from flask_limiter import Limiter


app = flask.Flask(__name__)
app.config.from_object("config")
limiter = Limiter(app)


@app.route('/<int:page>')
@app.route('/')
def posts(page=1):
    posts_per_page = app.config['POSTS_PER_PAGE']
    page -= 1  # maths
    offset = posts_per_page * page
    json_payload = json.dumps({'offset': offset,
                               'limit': posts_per_page})
    request = requests.get("http://localhost:5000/posts",
                           data=json_payload)
    posts = request.json()
    return flask.render_template('get_view.html',
                                 posts=posts)


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=8080)
