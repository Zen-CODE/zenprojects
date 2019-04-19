#!flask/bin/python
from flask import Flask, jsonify, make_response, send_file, render_template
from library import MusicLib
from os.path import expanduser, basename
from flask_httpauth import HTTPBasicAuth
from io import BytesIO
from mplayer import MPlayer


app = Flask(__name__)
""" The instance of the Flask application. """

lib = MusicLib(expanduser("~/Zen/Music/"))
""" An instance of the MusicLib to serve our library information. """

auth = HTTPBasicAuth()
""" Object handling out authentication """


@auth.get_password
def get_password(username):
    if username == 'bob':
        return 'chop'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/')
def index():
    return render_template('index.html')


# ==============================================================================
# API
# ==============================================================================
api_url = "/tunez/api/v1.0/"

# Library


@app.route(api_url + 'artists', methods=['GET'])
@auth.login_required
def get_artists():
    """
    Return a list of all the artists in our music library.
    """
    return jsonify({'artists': lib.get_artists()})


@app.route(api_url + 'albums/<artist>', methods=['GET'])
@auth.login_required
def get_albums(artist):
    """
    Return a list of albums by the specified artist.
    """
    return jsonify({'albums': lib.get_albums(artist)})


@app.route(api_url + 'tracks/<artist>/<album>', methods=['GET'])
@auth.login_required
def get_tracks(artist, album):
    """
    Return a list of tracks in the specified album.
    """
    return jsonify({'tracks': lib.get_tracks(artist, album)})


@app.route(api_url + 'cover/<artist>/<album>', methods=['GET'])
@auth.login_required
def get_cover(artist, album):
    """
    Return the cover image file. If there is none, return the default cover
    image.
    """
    cover = lib.get_cover(artist, album)
    file_name = cover if cover else "static/audio_icon.png"
    with open(file_name, 'rb') as f:
        return send_file(BytesIO(f.read()),
                         attachment_filename=file_name,
                         mimetype='image/png')

# Library


@app.route(api_url + 'player/volume_up', methods=['GET'])
def volume_up():
    """ Turn the volume up. """
    MPlayer().volume_up()
    return make_response("Success", 200)


@app.route(api_url + 'player/volume_down', methods=['GET'])
def volume_down():
    """ Turn the volume down. """
    MPlayer().volume_down()
    return make_response("Success", 200)


@app.route(api_url + 'player/stop', methods=['GET'])
def stop():
    """ Stop the currently active player. """
    MPlayer().stop()
    return make_response("Success", 200)


@app.route(api_url + 'player/play_pause', methods=['GET'])
def play_pause():
    """ Play or pause the currently active player. """
    MPlayer().play_pause()
    return make_response("Success", 200)


@app.route(api_url + 'player/next', methods=['GET'])
def next_track():
    """ Advance the player to the next track. """
    MPlayer().next_track()
    return make_response("Success", 200)


@app.route(api_url + 'player/previous', methods=['GET'])
def previous_track():
    """ Go back to the previous track. """
    MPlayer().previous_track()
    return make_response("Success", 200)


@app.route(api_url + 'player/cover', methods=['GET'])
def cover():
    """ Show the album cover. """
    _cover = MPlayer().cover()
    if cover:
        with open(_cover, 'rb') as f:
            return send_file(BytesIO(f.read()),
                             attachment_filename=basename(_cover),
                             mimetype='image/png')

    return make_response("Success, but no album cover for this baby...", 200)


if __name__ == '__main__':
    app.run(debug=True)
