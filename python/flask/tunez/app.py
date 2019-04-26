#!flask/bin/python
from flask import Flask, jsonify, make_response, send_file, render_template
from library import MusicLib
from os.path import expanduser, basename
from flask_httpauth import HTTPBasicAuth
from io import BytesIO
from mplayer import MPlayer
from flasgger import Swagger


app = Flask(__name__)
""" The instance of the Flask application. """

swagger = Swagger(app)
""" The Swagger UI app exposing the API documentation. Once running, go to:

    http://localhost:5000/apidocs/
 """

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
    ---
    definitions:
      Artists:
        type: object
        properties:
          artist_name:
            type: array
            items:
              $ref: '#/definitions/Artist'
      Artist:
        type: string
    responses:
      200:
        description: A list of all the artists in our library.
        schema:
          $ref: '#/definitions/Artists'
        examples:
          artists: ['Ace of Base', 'Affiance', 'In Flames']
    """
    return jsonify({'artists': lib.get_artists()})


@app.route(ZenTunez.get_route('albums/<artist>'), methods=['GET'])
@auth.login_required
def get_albums(artist):
    """
    Return a list of albums by the specified artist.
    ---
    parameters:
      - name: artist
        in: path
        type: string
        required: true
        description: The name of the artist for which to retrieve albums
    definitions:
      Albums:
        type: object
        properties:
          album_name:
            type: array
            items:
              $ref: '#/definitions/Album'
      Album:
        type: string
    responses:
      200:
        description: A list of all the album by this artist.
        schema:
          $ref: '#/definitions/Albums'
        examples:
          albums: ['Da Capo', 'Happy Nation', 'Flowers']
    """
    return jsonify({'albums': lib.get_albums(artist)})


@app.route(ZenTunez.get_route('tracks/<artist>/<album>'), methods=['GET'])
@auth.login_required
def get_tracks(artist, album):
    """
    Return a list of tracks in the specified album.
    ---
    parameters:
      - name: artist
        in: path
        type: string
        required: true
        description: The name of the artist of the album
      - name: album
        in: path
        type: string
        required: true
        description: The name of the album for which to retrieve tracks
    definitions:
      Tracks:
        type: object
        properties:
          track_name:
            type: array
            items:
              $ref: '#/definitions/Track'
      Track:
        type: string
    responses:
      200:
        description: A list of all the tracks on this album.
        schema:
          $ref: '#/definitions/Tracks'
        examples:
          tracks: ['01 - Premonition.mp3', '02 - Astronomical Unit.mp3',
                   '03 - Julia.mp3']
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
    mplayer = MPlayer()

    @staticmethod
    def _get_return():
        """ Get the state of the audio player and return it in the response"""
        return ZenTunez.get_response(AudioPlayer.mplayer.get_state())

    @staticmethod
    @app.route(ZenTunez.get_route('player/volume_up'), methods=['GET'])
    def volume_up():
        """ Turn the volume up. """
        AudioPlayer.mplayer.volume_up()
        return AudioPlayer._get_return()

    @staticmethod
    @app.route(ZenTunez.get_route('player/volume_down'), methods=['GET'])
    def volume_down():
        """ Turn the volume down. """
        MPlayer().volume_down()
        return AudioPlayer._get_return()

    @staticmethod
    @app.route(ZenTunez.get_route('player/stop'), methods=['GET'])
    def stop():
        """ Stop the currently active player. """
        MPlayer().stop()
        return AudioPlayer._get_return()

    @staticmethod
    @app.route(ZenTunez.get_route('player/play_pause'), methods=['GET'])
    def play_pause():
        """ Play or pause the currently active player. """
        MPlayer().play_pause()
        return AudioPlayer._get_return()

    @staticmethod
    @app.route(ZenTunez.get_route('player/next'), methods=['GET'])
    def next_track():
        """ Advance the player to the next track. """
        MPlayer().next_track()
        return AudioPlayer._get_return()

    @staticmethod
    @app.route(ZenTunez.get_route('player/previous'), methods=['GET'])
    def previous_track():
        """ Go back to the previous track. """
        MPlayer().previous_track()
        return AudioPlayer._get_return()

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

    @staticmethod
    @app.route(ZenTunez.get_route('player/state'), methods=['GET'])
    def state():
        """ Show the album cover. """
        return AudioPlayer._get_return()


if __name__ == '__main__':
    app.run(debug=True)
