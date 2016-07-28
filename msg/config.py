REDIS_URL = "redis://localhost"
SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
SLEEP_RATE = 0.2
ERROR_404_HELP = False

JSON_SCHEMA_DIR = "schema"
"""str: path to directory containing json schemas.

flask-jsonschema
"""

# Limiting: limit the number of REST requests,
# implemented with flask_limiter:
#
#   https://flask-limiter.readthedocs.io/en/stable/
LIMITS_GLOBAL = ["200 per day", "50 per hour"]
"""List(str): A list of limits according to the
flask_limiter API docs.

The maximum number of requests period. 
"""

LIMITS_USER_GET = "1 per second"
"""str: flask_limiter limit.

Limit the rate which an IP may request
user information.
"""

LIMITS_USER_POST = "2 per minute"
"""str: flask_limiter limit.

Limit the number of users an IP
may create per second.
"""

LIMITS_MESSAGES_GET = "10 per minute"
"""str: flask_limiter limit.

Limit the rate which an IP may request
a range of messages.
"""

LIMITS_MESSAGES_GET_LIMIT = 20
"""int: Maximum number of messages per request."""

LIMITS_MESSAGE_PUT = "10 per minute"
"""str: flask_limiter limit.

Limit the rate which an IP may request
changing a message's information.
"""

LIMITS_MESSAGE_POST = "10 per minute"
"""str: flask_limiter limit.

Limit the rate which an IP may create
new messages.
"""

LIMITS_MESSAGE_DELETE = "5 per minute"
"""str: flask_limiter limit.

Limit the rate which an IP may delete
messages.
"""

LIMITS_MESSAGE_GET = "100 per second"
"""str: flask_limiter rate limit.

Limit the rate which an IP may get
a specific message.
"""

LIMITS_STREAM_GET = "100 per second"
"""str: flask_limiter rate limit.

Limit the rate of events sent to a client.
"""
