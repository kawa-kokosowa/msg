# msg

[![Travis CI Status](https://travis-ci.org/lily-seabreeze/msg.svg)](https://travis-ci.org/lily-seabreeze/msg)
[![Coveralls Code Coverage](https://img.shields.io/coveralls/lily-seabreeze/msg.svg)](https://coveralls.io/github/lily-seabreeze/msg)

msg is a simple, but powerful RESTful [service-oriented architecture (SOA)](https://en.wikipedia.org/wiki/Service-oriented_architecture)
messaging library.

msg focuses on the overlapping core features of any messaging system,
so you can skip to implementing the cool parts. You can use msg to
build live chat/instant messenger, a forum, a Twitter clone, a blog, etc.

msg runs in Python 2 and 3. msg can be configured to use
any database supported by SQLAlchemy.

The beauty in this project is that its focus/scope is tiny, the barebones
of any messaging system, which we perfect for you.

For the REST API, setup instructions, deployment instructions, and more,
please read [The Official msg Wiki](https://github.com/lily-seabreeze/msg/wiki)!

## Generic setup

  1. install and launch redis server
  2. Edit `msg/config.py` or override
  3. `pip install -r requirements/base.txt`
  4. `gunicorn msg.msg:app --worker-class gevent --bind localhost:5000`

If you're using a non-default database:

`python -c "import msg.msg; msg.msg.init_db()"`


## Test it out

For the demo to work you need to install the
`Allow-Control-Allow-Origin: *` plugin for Firefox,
Chrome, whatever.

  1. `cd examples`
  2. `python msgviewer.py`
  3. Checkout http://localhost:8080/ and http://localhost:8080/stream

If you're using `httpie` (`sudo apt install httpie`) here are some example commands:

  4. Create a user: `http POST localhost:5000/user username=kitten password=yarn`
  5. Create a message: `http POST localhost:5000/message text="i love kittens" --auth kitten:yarn`
