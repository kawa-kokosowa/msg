# msgboard

[![Travis CI Status](https://travis-ci.org/lily-seabreeze/msgboard.svg)](https://travis-ci.org/lily-seabreeze/msgboard)
[![Coveralls Code Coverage](https://img.shields.io/coveralls/lily-seabreeze/msgboard.svg)](https://coveralls.io/github/lily-seabreeze/msgboard)

msgboard is a simple, but powerful RESTful [service-oriented architecture (SOA)](https://en.wikipedia.org/wiki/Service-oriented_architecture)
messaging library.

msgboard focuses on the overlapping core features of any messaging system,
so you can skip to implementing the cool parts. You can use msgboard to
build live chat/instant messenger, a forum, a Twitter clone, a blog, etc.

msgboard runs in Python 2 and 3. msgboard can be configured to use
any database supported by SQLAlchemy.

The beauty in this project is that its focus/scope is tiny, the barebones
of any messaging system, which we perfect for you.

For the REST API, setup instructions, deployment instructions, and more,
please read [The Official msgboard Wiki](https://github.com/lily-seabreeze/msgboard/wiki)!

## Generic setup

  1. install and launch redis server
  2. `pip install -r requirements/base.txt`
  2. `gunicorn msgboard.msg:app --worker-class gevent --bind localhost:5000`

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
