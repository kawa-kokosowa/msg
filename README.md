# msgboard

[![Travis CI Status](https://travis-ci.org/lillian-gardenia-seabreeze/msgboard.svg)](https://travis-ci.org/lillian-gardenia-seabreeze/msgboard)
[![Coveralls Code Coverage](https://img.shields.io/coveralls/lillian-gardenia-seabreeze/msgboard.svg)](https://coveralls.io/github/lillian-gardenia-seabreeze/msgboard)

msgboard is a RESTful messaging solution, implemented in Python,
with user accounts; ability to edit, delete, and submit posts.

msgboard is general purpose, it could be used for an instant
message service, a forum, or really anything else that is
message-based (e.g., Twitter!).

The point of this project is to create an elegant, efficient,
and intuitive barebones, tiny-scoped message library for general
use in web development.

## Features

  * RESTful
  * Has functioning event stream, with documentation
  * Works in both Python 2 and Python 3
  * Use any database supported by SQLAlchemy
  * Easy to configure
  * Rate limiting
  * Post/edit/delete messages
  * Users
  * Thoroughly tested, stable

## Deploying

I wrote [a blog post on setting up a gevent/Flask app on FreeBSD
with `supervisord` and `nginx`](http://hypatiasoftware.org/2016/01/29/polling-is-a-hack-server-sent-events-eventsource-with-gevent-flask-nginx-and-freebsd/).
