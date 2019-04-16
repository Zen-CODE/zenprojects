#!flask/bin/python
from flask import Flask, jsonify, make_response, send_file
from library import MusicLib
from os.path import expanduser
from flask_httpauth import HTTPBasicAuth
from io import BytesIO


albums = [
    {
        'artist': 'Ace Of Base',
        'album': 'Da Capo'
    },
    {
        'artist': 'Astrix',
        'album': 'Artcore'
    }
]

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
    return "Hello, World!"


@app.route('/tunez/api/v1.0/artists', methods=['GET'])
@auth.login_required
def get_artists():
    return jsonify({'artists': lib.get_artists()})


@app.route('/tunez/api/v1.0/albums/<artist>', methods=['GET'])
@auth.login_required
def get_albums(artist):
    return jsonify({'artists': lib.get_albums(artist)})


@app.route('/tunez/api/v1.0/tracks/<artist>/<album>', methods=['GET'])
@auth.login_required
def get_tracks(artist, album):
    return jsonify({'artists': lib.get_tracks(artist, album)})


@app.route('/tunez/api/v1.0/cover/<artist>/<album>', methods=['GET'])
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


if __name__ == '__main__':
    app.run(debug=True)
