"""
This module houses the Cloud Firestore functions, providing methods to read,
write and listen for data changes.
"""
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class NowPlaying:
    """
    This class defines the model mapping the 'Now Playing' entries to the
    FireStore database table.

    Note: When instantiating this class, the constructor keyword arguments
          must contain at least the following keys:

            'artist', 'album', 'track', 'state', 'machine', 'datetime'
    """

    _client = None
    """ The singleton firestore client instance. """

    fields = ['artist', 'album', 'track', 'state', 'machine', 'datetime']

    def __init__(self, **kwargs):
        if self._client is None:
            NowPlaying._client = self._get_client()
        self.props = kwargs

    @staticmethod
    def _get_client():
        """ Generate and return a FireStore client using the service account.
        """
        cred = credentials.Certificate('keys/tunez-245820-047b7b31e116.json')
        firebase_admin.initialize_app(cred)
        return firestore.client()

    def __repr__(self):
        return "<NowPlaying on {machine}: {artist},  {album}: {track}, state=" \
               "{state} @{datetime}".format(**self.props)

    def save(self):
        """ Store the item to Firestore """
        doc_ref = self._client.collection('tunez').document('now_playing')
        doc_ref.set(self.props)


if __name__ == "__main__":
    from datetime import datetime
    obj = NowPlaying(
        artist="Us3",
        album="Cantaloop 2004",
        track="01 - Cantaloop 2004 Soul.mp3",
        state="playing",
        machine="zenbox",
        date=datetime.now())
    obj.save()

