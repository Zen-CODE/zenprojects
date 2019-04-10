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


class TunezApp(object):
    """
    The main Application object, managing object instantiation and shared
    data.
    """

    app = Flask(__name__)
    """ The instance of the Flask application. """

    def __init__(self):
        super(TunezApp, self).__init__()
        self.lib = MusicLib(expanduser("~/Zen/Music/"))

    @staticmethod
    @app.route('/')
    def index():
        return "Hello, World!"

    @staticmethod
    @app.route('/tunez/api/v1.0/albums', methods=['GET'])
    def get_albums():
        return jsonify({'albums': albums})


if __name__ == '__main__':
    TunezApp().app.run(debug=True)
