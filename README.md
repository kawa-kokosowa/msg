# msgboard

[![Travis CI Status](https://travis-ci.org/lillian-gardenia-seabreeze/msgboard.svg)](https://travis-ci.org/lillian-gardenia-seabreeze/msgboard)
[![Coveralls Code Coverage](https://img.shields.io/coveralls/lillian-gardenia-seabreeze/msgboard.svg)](https://coveralls.io/github/lillian-gardenia-seabreeze/msgboard)

msgboard is a simple, but powerful RESTful [service-oriented architecture (SOA)](https://en.wikipedia.org/wiki/Service-oriented_architecture)
messaging library.

msgboard focuses on the overlapping core features of any messaging system,
so you can skip to implementing the cool parts. You can use msgboard to
build live chat/instant messenger, a forum, a Twitter clone, a blog, etc.

msgboard runs in Python 2 and 3. msgboard can be configured to use
any database supported by SQLAlchemy.

The beauty in this project is that its focus/scope is tiny, the barebones
of any messaging system, which we perfect for you.

## Test it out!

Start the msg server with:

`python -m msgboard.msg init_db`

Your API root is http://localhost:5000/

If you're using `httpie` here are some example commands:

  1. Create a user: `http POST localhost:5000/user username=kitten password=yarn`
  2. Create a message: `http POST localhost:5000/message text="i love kittens" --auth kitten:yarn`

Also, check out the `example/` directory!

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

  * `http GET localhost:5000/user/1`
  * `http GET localhost:5000/user/kitten`

Successful response:

```
{
    "bio": null,
    "created": "2016-07-23T22:00:06.467591Z",
    "id": 1,
    "username": "kitten"
}
```

Responds with a 400 if you neglected to specify a `user_id` or `username`.

Responds with 404 if you lookup a `user_id` or `username` that doesn't exist.

#### Post

Create a new user.

HTTPie examples:

  * `http POST localhost:5000/user username=kitten password=yarn bio="A cute ittle kitten."`

Successful response:

```
{
    "bio": "A cute ittle kitten.",
    "created": "2016-07-24T01:19:58.581466Z",
    "id": 1,
    "username": "kitten"
}
```

Will respond with 400 if username already exists, or if username and
password wasn't specified.

### Messages

*Endpoint*: `/messages`

Manage more than one message at a time!

#### Get

Get a range of messages using a "limit" and an "offset."

HTTPie examples:

  * `http GET localhost:5000/messages limit=10 offset=20`

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

Successful response:

```
{
    "created": "2016-07-24T01:25:20.637226Z",
    "id": 1,
    "text": "I love kittens",
    "user": {
        "bio": "A cute ittle kitten.",
        "created": "2016-07-24T01:19:58.581466Z",
        "id": 1,
        "username": "kitten"
    }
}
```

Will return a 400 if `text` was not specified.

Will return 401 if not authorized.

#### Delete

Remove an existing message!

HTTPie examples:

  * `http DELETE localhost:5000/message/1 --auth kitten:yarn`

Successful response:

```
{}
```

Will return 401 if not authorized.

Will return 400 if the ID does not match any message in the database.

#### Get

Get a single, specific message.

HTTPie examples:

  * `http GET localhost:5000/message/1`

Successful response:

```
{
    "created": "2016-07-24T01:33:42.592946Z",
    "id": 1,
    "text": "I love kittens",
    "user": {
        "bio": "A cute ittle kitten.",
        "created": "2016-07-24T01:32:15.596500Z",
        "id": 1,
        "username": "kitten"
    }
}
```

Will return 404 if provided ID does not exist in database.

### Stream

*Endpoint:* `/stream`

Used for JavaScript EventStream. Listen with EvenStream to get
new message events.

Example event:

```
{
    "created": "2016-07-24T01:33:42.592946Z",
    "id": 1,
    "text": "I love kittens",
    "user": {
        "bio": "A cute ittle kitten.",
        "created": "2016-07-24T01:32:15.596500Z",
        "id": 1,
        "username": "kitten"
    }
}
```
