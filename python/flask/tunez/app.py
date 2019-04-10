#!flask/bin/python
from flask import Flask, jsonify
from library import MusicLib
from os.path import expanduser

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


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/tunez/api/v1.0/artists', methods=['GET'])
def get_artists():
    return jsonify({'artists': lib.get_artists()})


@app.route('/tunez/api/v1.0/albums/<artist>', methods=['GET'])
def get_albums(artist):
    return jsonify({'artists': lib.get_albums(artist)})


if __name__ == '__main__':
    app.run(debug=True)
