# REST Docs

## User

*Endpoint*: `/user`

This endpoint is used for managing a user account.

### Get

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

### Post

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

## Messages

*Endpoint*: `/messages`

Manage more than one message at a time!

### Get

Get a range of messages using a "limit" and an "offset."

HTTPie examples:

  * `http GET localhost:5000/messages limit=10 offset=20`

## Message

*Endpoint*: `/message`

Manage a single message!

### Put

Edit an existing message.

HTTPie examples:

  * `http PUT localhost:5000/message/1 text="New text!" --auth kitten:yarn`

### Post

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

### Delete

Remove an existing message!

HTTPie examples:

  * `http DELETE localhost:5000/message/1 --auth kitten:yarn`

Successful response:

```
{}
```

Will return 401 if not authorized.

Will return 400 if the ID does not match any message in the database.

### Get

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

## Stream

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
