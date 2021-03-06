#!flask/bin/python
from flask import Flask, jsonify, make_response, send_file, render_template
from library import MusicLib
from os.path import expanduser, basename
from flask_httpauth import HTTPBasicAuth
from io import BytesIO
from mplayer import MPlayer
from flasgger import Swagger
from json import loads


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
    base_url = "/tunez/"

    def __init__(self):
        """ Initialise the class and bind the used method to the corresponding
        routes of out Flask app.

        :param: app - the Flask application object.
        """
        app = Flask(__name__)
        """ The instance of the Flask application. """

        AudioPlayer(app, self.base_url)
        LibraryServer(app, self.base_url)
        self.init_swagger(app)
        self.app = app

    @staticmethod
    def init_swagger(app):
        """
        Initialize the Swagger UI application and configuration
        """
        with open("swagger.template.json", "rb") as f:
            swagger = Swagger(app, template=loads(f.read()))
        """ The Swagger UI app exposing the API documentation. Once running, go to:

            http://localhost:5000/apidocs/
         """

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

    def run(self):
        """ Run the application as a Falsk server. """
        self.app.run(debug=True, host="0.0.0.0")


class AudioPlayer:
    """
    This class handles the sending of commands to the currently playing
    MPris2 audio player and the retrieving of information from it.
    """

    def __init__(self, app, base_url):
        """ Initialise the class and bind the used method to the corresponding
        routes of out Flask app.

        :param: app - the Flask application object.
        :route: string - The base_url user to serve the web application
        """
        self.mplayer = MPlayer()
        route = base_url + "player/"
        app.add_url_rule(route , "player/",
                         lambda: render_template('index.html'), methods=['GET'])
        for meth in ["state", "cover", "previous", "next", "play_pause", "stop",
                     "volume_up", "volume_down"]:
            app.add_url_rule(route + meth, "player/" + meth,
                             getattr(self, meth), methods=['GET'])

    def _get_return(self):
        """ Get the state of the audio player and return it in the response"""
        return ZenTunez.get_response(self.mplayer.get_state())

    def volume_up(self):
        """
        Turn the volume up.
        ---
        tags:
            - MPris2 Audio player
        responses:
          200:
            description: Success if we have turned up the volume.
            schema:
              $ref: '#/definitions/PlayerMetadata'
        """
        self.mplayer.volume_up()
        return self._get_return()

    def volume_down(self):
        """
        Turn the volume down.
        ---
        tags:
            - MPris2 Audio player
        responses:
          200:
            description: Success if we have turned down the volume.
            schema:
              $ref: '#/definitions/PlayerMetadata'
        """
        self.mplayer.volume_down()
        return self._get_return()

    def stop(self):
        """
        Stop the currently active player.
        ---
        tags:
            - MPris2 Audio player
        responses:
          200:
            description: Success if we have stopped the player.
            schema:
              $ref: '#/definitions/PlayerMetadata'
        """
        self.mplayer.stop()
        return self._get_return()

    def play_pause(self):
        """
        Play or pause the currently active player.
        ---
        tags:
            - MPris2 Audio player
        responses:
          200:
            description: Success if we have played or paused the current player.
            schema:
              $ref: '#/definitions/PlayerMetadata'
        """
        self.mplayer.play_pause()
        return self._get_return()

    def next(self):
        """
        Advance the player to the next track.
        ---
        tags:
            - MPris2 Audio player
        responses:
          200:
            description: Success if we have moved to the next track.
            schema:
              $ref: '#/definitions/PlayerMetadata'
        """
        self.mplayer.next_track()
        return self._get_return()

    def previous(self):
        """
        Go back to the previous track.
        ---
        tags:
            - MPris2 Audio player
        responses:
          200:
            description: Success if we have moved to the previous track.
            schema:
              $ref: '#/definitions/PlayerMetadata'
        """
        self.mplayer.previous_track()
        return self._get_return()

    def cover(self):
        """
        Return the album cover.
        ---
        tags:
            - MPris2 Audio player
        responses:
            '200':
              description: The cover image
              content:
                image/png:
                  schema:
                    type: string
                    format: binary

        """
        _cover = self.mplayer.cover()
        if _cover:
            with open(_cover, 'rb') as f:
                return send_file(BytesIO(f.read()),
                                 attachment_filename=basename(_cover),
                                 mimetype='image/png')
        return ZenTunez.get_response(
            "Success, but no album cover for this baby...")

    def state(self):
        """
        Return a json dictionary with information on the state of the current
        plater
        ---
        tags:
            - MPris2 Audio player
        definitions:
          PlayerMetadata:
            type: object
            properties:
              track:
                type: string
                description: The name of the currently playing track
              artist:
                type: string
                description: The artist of the currently playing track
              album:
                type: string
                description: The album of the currently playing track
              state:
                type: string
                description: The state of the player. One on 'Playing',
                             'Stopped' or 'Paused'
              volume:
                type: number
                description: The volume as a percentage
              position:
                type: number
                description: The position in the currently playing track as a
                             percentage
        responses:
          200:
            description: Success if we have moved to the previous track.
            schema:
              $ref: '#/definitions/PlayerMetadata'
        """
        return self._get_return()


class LibraryServer(object):
    """
    This class manages the interaction around the MusicLibrary object. This
    includes the retrieving of data and the serving of the Swagger UI
    documentation.
    """
    def __init__(self, app, base_url):
        """ Initialise the class and bind the used method to the corresponding
        routes of out Flask app.

        :param: app - the Flask application object.
        :base_url: string - The base_url user to serve the web application
        """
        route = base_url + "library/"
        app.add_url_rule(route + 'artists', "library/artists",
                         self.artists, methods=['GET'])
        app.add_url_rule(route + 'albums/<artist>', "library/albums",
                         self.albums, methods=['GET'])
        app.add_url_rule(route + 'tracks/<artist>/<album>', "library/tracks",
                         self.tracks, methods=['GET'])
        app.add_url_rule(route + 'cover/<artist>/<album>', "library/cover",
                         self.cover, methods=['GET'])
        self.lib = MusicLib(expanduser("~/Zen/Music/"))
        """ An instance of the MusicLib to serve our library information. """

    @auth.login_required
    def artists(self):
        """
        Return a list of all the artists in our music library.
        ---
        tags:
            - Music Library
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
        return jsonify({'artists': self.lib.get_artists()})

    @auth.login_required
    def albums(self, artist):
        """
        Return a list of albums by the specified artist.
        ---
        tags:
            - Music Library
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
        return jsonify({'albums': self.lib.get_albums(artist)})

    @auth.login_required
    def tracks(self, artist, album):
        """
        Return a list of tracks in the specified album.
        ---
        tags:
            - Music Library
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
        return jsonify({'tracks': self.lib.get_tracks(artist, album)})

    @staticmethod
    @auth.login_required
    def cover(self, artist, album):
        """
        Return the cover image file. If there is none, return the default cover
        image.
        ---
        tags:
            - Music Library
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
        _cover = self.lib.get_cover(artist, album)
        file_name = _cover if _cover else "static/audio_icon.png"
        with open(file_name, 'rb') as f:
            return send_file(BytesIO(f.read()),
                             attachment_filename=file_name,
                             mimetype='image/png')


if __name__ == '__main__':
    ZenTunez().run()
