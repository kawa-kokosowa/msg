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

## Test it out!

Start the msg server with:

`python -m msgboard.msg init_db`

Your API root is http://localhost:5000/

If you're using `httpie` here are some example commands:

  1. Create a user: `http POST localhost:5000/user username=kitten password=yarn`
  2. Create a message: `http POST localhost:5000/message text="i love kittens" --auth kitten:yarn`

## Deploying

I wrote [a blog post on setting up a gevent/Flask app on FreeBSD
with `supervisord` and `nginx`](http://hypatiasoftware.org/2016/01/29/polling-is-a-hack-server-sent-events-eventsource-with-gevent-flask-nginx-and-freebsd/).

## REST Docs

### User

*Endpoint*: `/user`

This endpoint is used for managing a user account.

#### Get

Fetch a user by `user_id` or `username`.

HTTPie examples:

  * http GET localhost:5000/user/1
  * http GET localhost:5000/user/kitten

#### Post

Create a new user.

HTTPie examples:

  * `http POST localhost:5000/user username=kitten password=yarn bio="A cute ittle kitten."`

### Messages

*Endpoint*: `/messages`

Manage more than one message at a time!

#### Get

Get a range of messages using a "limit" and an "offset."

HTTPie examples:

  * `HTTP GET localhost:5000/messages limit=10 offset=20`

### Message

*Endpoint*: `/message`

Manage a single message!

#### Put

Edit an existing message.

HTTPie examples:

  * `http PUT localhost:5000/message/1 text="New text!" --auth kitten:yarn`

#### Post

Create a new message!

HTTPie examples:

  * `http POST localhost:5000/message text="I love kittens!" --auth kitten:yarn`

#### Delete

Remove an existing message!

HTTPie examples:

  * `http DELETE localhost:5000/message/1 --auth kitten:yarn`

#### Get

Get a single, specific message.

HTTPie examples:

  * `http GET localhost:5000/message/1`

### Stream

*Endpoint:* `/stream`

Used for JavaScript EventStream. Listen with EvenStream to get
new message events.
