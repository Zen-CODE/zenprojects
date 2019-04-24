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
class ZenTunez(object):
    """
    The main application class
    """
    api_url = "/tunez/api/v1.0/"

    @staticmethod
    def get_route(path):
        """
        Return the fully qualified path to the API,
        """
        return ZenTunez.api_url + path

    @staticmethod
    def get_response(data_dict=None, code=200):
        """
        Generate and return the appropriate HTTP response object containing the
        json version of the *data_dict" dictionary.
        """
        if data_dict is None:
            data_dict = {"message": "Success"}

        resp = make_response(jsonify(data_dict), code)
        resp.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        return resp

# Library


@app.route(ZenTunez.get_route('artists'), methods=['GET'])
@auth.login_required
def get_artists():
    """
    Return a list of all the artists in our music library.
    """
    return jsonify({'artists': lib.get_artists()})


@app.route(ZenTunez.get_route('albums/<artist>'), methods=['GET'])
@auth.login_required
def get_albums(artist):
    """
    Return a list of albums by the specified artist.
    """
    return jsonify({'albums': lib.get_albums(artist)})


@app.route(ZenTunez.get_route('tracks/<artist>/<album>'), methods=['GET'])
@auth.login_required
def get_tracks(artist, album):
    """
    Return a list of tracks in the specified album.
    """
    return jsonify({'tracks': lib.get_tracks(artist, album)})


@app.route(ZenTunez.get_route('cover/<artist>/<album>'), methods=['GET'])
@auth.login_required
def get_cover(artist, album):
    """
    Return the cover image file. If there is none, return the default cover
    image.
    """
    _cover = lib.get_cover(artist, album)
    file_name = _cover if _cover else "static/audio_icon.png"
    with open(file_name, 'rb') as f:
        return send_file(BytesIO(f.read()),
                         attachment_filename=file_name,
                         mimetype='image/png')

# Library


class AudioPlayer:
    """
    This class handles the sending of commands to the currently playing
    MPris2 audio player and the retrieving of information from it.
    """

    @staticmethod
    @app.route(ZenTunez.get_route('player/volume_up'), methods=['GET'])
    def volume_up():
        """ Turn the volume up. """
        MPlayer().volume_up()
        return ZenTunez.get_response()

    @staticmethod
    @app.route(ZenTunez.get_route('player/volume_down'), methods=['GET'])
    def volume_down():
        """ Turn the volume down. """
        MPlayer().volume_down()
        return ZenTunez.get_response()

    @staticmethod
    @app.route(ZenTunez.get_route('player/stop'), methods=['GET'])
    def stop():
        """ Stop the currently active player. """
        MPlayer().stop()
        return ZenTunez.get_response()

    @staticmethod
    @app.route(ZenTunez.get_route('player/play_pause'), methods=['GET'])
    def play_pause():
        """ Play or pause the currently active player. """
        MPlayer().play_pause()
        return ZenTunez.get_response()

    @staticmethod
    @app.route(ZenTunez.get_route('player/next'), methods=['GET'])
    def next_track():
        """ Advance the player to the next track. """
        MPlayer().next_track()
        return ZenTunez.get_response()

    @staticmethod
    @app.route(ZenTunez.get_route('player/previous'), methods=['GET'])
    def previous_track():
        """ Go back to the previous track. """
        MPlayer().previous_track()
        return ZenTunez.get_response()

    @staticmethod
    @app.route(ZenTunez.get_route('player/cover'), methods=['GET'])
    def cover():
        """ Show the album cover. """
        _cover = MPlayer().cover()
        if _cover:
            with open(_cover, 'rb') as f:
                return send_file(BytesIO(f.read()),
                                 attachment_filename=basename(_cover),
                                 mimetype='image/png')
        return ZenTunez.get_response(
            "Success, but no album cover for this baby...")


if __name__ == '__main__':
    app.run(debug=True)
