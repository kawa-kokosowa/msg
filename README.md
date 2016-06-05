# msgboard

A modern imageboard.

The html/frontend stuff is ran on a server called `msgviewer.py`.

The actual magic is done through the api server, called `api/msgboard.py`.

## Test it out

  - `python api/msgboard.py init_db`
  - `python msgviewer.py`
  - Open http://localhost:8080/ in web browser with
    `Allow-Control-Origin: *`, which you need for
    testing server sent events locally. There's a
    [Chrome Plugin for `Allow-Control-Origin: *`](https://chrome.google.com/webstore/detail/allow-control-allow-origi/nlfbmbojpeacfghkpbjhddihlkkiljbi/related?hl=en)
    
## Plans

Here are the features I'm hoping to implement:

  * Nice jinja views for restful calls
  * Support for checking links, replacing/adding
    embed for music, video, or picture (javascript)
