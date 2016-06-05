# msgboard API Server

This directory contains the `msgboard` API server, meaning
the bulk of the app. Whereas `msgviewer`, in the root of
this project, is simply a web interface which utilizes
the `msgboard` API server.

The `msgboard` API server uses `gevent` and its uWSGI server.

## Deploying

I wrote [a blog post on setting up a gevent/Flask app on FreeBSD
with `supervisord` and `nginx`](http://hypatiasoftware.org/2016/01/29/polling-is-a-hack-server-sent-events-eventsource-with-gevent-flask-nginx-and-freebsd/).
