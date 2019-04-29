#!flask/bin/python
from flask import Flask, jsonify, make_response, send_file, render_template
from library import MusicLib
from os.path import expanduser, basename
from flask_httpauth import HTTPBasicAuth
from io import BytesIO
from mplayer import MPlayer
from flasgger import Swagger
from json import loads


app = Flask(__name__)
""" The instance of the Flask application. """

with open("swagger.template.json", "rb") as f:
    swagger = Swagger(app, template=loads(f.read()))
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


# ==============================================================================
# API
# ==============================================================================
class ZenTunez(object):
    """
    The main application class
    """
    def __init__(self, app, route):
        """ Initialise the class and bind the used method to the corresponding
        routes of out Flask app.

        :param: app - the Flask application object.
        """
        route = route + "library/"
        app.add_url_rule(route + 'artists', "library/artists",
                         self.artists, methods=['GET'])
        app.add_url_rule(route + 'albums/<artist>', "library/albums",
                         self.albums, methods=['GET'])
        app.add_url_rule(route + 'tracks/<artist>/<album>', "library/tracks",
                         self.tracks, methods=['GET'])
        app.add_url_rule(route + 'cover/<artist>/<album>', "library/cover",
                         self.cover, methods=['GET'])

    @staticmethod
    def get_response(data_dict=None, code=200):
        """
        Generate and return the appropriate HTTP response object containing the
        json version of the *data_dict" dictionary.
        """
        if data_dict is None:
            data_dict = {"message": "Success"}

        resp = make_response(jsonify(data_dict), code)
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp

    @staticmethod
    @auth.login_required
    def artists():
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

    @staticmethod
    @auth.login_required
    def albums(artist):
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

    @staticmethod
    @auth.login_required
    def tracks(artist, album):
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

    @staticmethod
    @auth.login_required
    def cover(artist, album):
        """
        Return the cover image file. If there is none, return the default cover
        image.
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
            description: The name of the album for which to retrieve the cover
        responses:
            '200':
              description: The cover image
              content:
                image/png:
                  schema:
                    type: string
                    format: binary
        """
        _cover = lib.get_cover(artist, album)
        file_name = _cover if _cover else "static/audio_icon.png"
        with open(file_name, 'rb') as f:
            return send_file(BytesIO(f.read()),
                             attachment_filename=file_name,
                             mimetype='image/png')


class AudioPlayer:
    """
    This class handles the sending of commands to the currently playing
    MPris2 audio player and the retrieving of information from it.
    """

    def __init__(self, app, route):
        """ Initialise the class and bind the used method to the corresponding
        routes of out Flask app.

        :param: app - the Flask application object.
        """
        self.mplayer = MPlayer()
        app.add_url_rule(route + "player/", "player/",
                         lambda: render_template('index.html'), methods=['GET'])
        for meth in ["state", "cover", "previous", "next", "play_pause", "stop",
                     "volume_up", "volume_down"]:
            app.add_url_rule(
                route + "player/" + meth, "player/" + meth, getattr(self, meth),
                methods=['GET'])

    def _get_return(self):
        """ Get the state of the audio player and return it in the response"""
        return ZenTunez.get_response(self.mplayer.get_state())

    def volume_up(self):
        """ Turn the volume up. """
        self.mplayer.volume_up()
        return self._get_return()

    def volume_down(self):
        """ Turn the volume down. """
        self.mplayer.volume_down()
        return self._get_return()

    def stop(self):
        """ Stop the currently active player. """
        self.mplayer.stop()
        return self._get_return()

    def play_pause(self):
        """ Play or pause the currently active player. """
        self.mplayer.play_pause()
        return self._get_return()

    def next(self):
        """ Advance the player to the next track. """
        self.mplayer.next_track()
        return self._get_return()

    def previous(self):
        """ Go back to the previous track. """
        self.mplayer.previous_track()
        return self._get_return()

    def cover(self):
        """ Show the album cover. """
        _cover = self.mplayer.cover()
        if _cover:
            with open(_cover, 'rb') as f:
                return send_file(BytesIO(f.read()),
                                 attachment_filename=basename(_cover),
                                 mimetype='image/png')
        return ZenTunez.get_response(
            "Success, but no album cover for this baby...")

    def state(self):
        """ Show the album cover. """
        return self._get_return()


AudioPlayer(app, "/tunez/api/v1.0/")
ZenTunez(app, "/tunez/api/v1.0/")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
