#!flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)


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


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/tunez/api/v1.0/albums', methods=['GET'])
def get_albums():
    return jsonify({'albums': albums})


if __name__ == '__main__':
    app.run(debug=True)
