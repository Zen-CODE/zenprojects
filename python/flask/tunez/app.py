#!flask/bin/python
from flask import Flask, jsonify, make_response, abort
from library import MusicLib
from os.path import expanduser, exists
from flask_httpauth import HTTPBasicAuth


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
    cover = lib.get_cover(artist, album)
    if cover:
        return jsonify({'cover': cover})
    else:        
        abort(404)  # Not found


if __name__ == '__main__':
    app.run(debug=True)
