from os.path import join, expanduser, exists
from components.filesystemextractor import FileSystemExtractor \
    as fse
import pandas as pd


class Library:
    """
    Class for fetching information about our music library. This information
    is built from the folder structure and filenames and used to populate a
    Pandas DataFrame for access and analysis.

    Args:
        config (dict): A dictionary with config. The following keys are used:
                       * `library_folder` - the path Music files.
                       ( )
                        `zenplayer.json` to store                        state between instan
    """

    def __init__(self, config={}):
        self.path = path = expanduser(
            config.get("library_folder", "~/Zen/Music"))
        """ The fully expanded path to the music libary folder."""

        self.data_frame = self._get_data_frame(path)
        """ A Pandas :class:`DataFrame` containing our library data as 'Artist',
        'Album', 'Track', and 'Cover' columns. """

    @staticmethod
    def _get_data_frame(path):
        """ Return a pandas DataFrame with 'Artist', 'Album', 'Track', and
        'Cover' columns.
        """
        artists, albums, tracks, covers = [], [], [], []
        for artist in fse.get_dirs(path):
            artist_path = join(path, artist)
            for album in fse.get_dirs(artist_path):
                _tracks, _covers = fse.get_media(
                    join(artist_path, album))
                for track in _tracks:
                    artists.append(artist)
                    albums.append(album)
                    tracks.append(track)
                    covers.append(_covers[0] if _covers else "")
        return pd.DataFrame({"Artist": artists, "Album": albums,
                             "Track": tracks, "Cover":  covers})

    def get_artists(self):
        """ Return a list of artists. """
        return list(self.data_frame.Artist.unique())

    def get_albums(self, artist):
        """ Return a list of albums for the *artist*. """
        return list(self.data_frame[
            self.data_frame["Artist"] == artist].Album.unique())

    def get_cover_path(self, artist, album):
        """ Return the album cover art for the given artist and album. """
        albums = self.data_frame[self.data_frame["Artist"] == artist]
        listing = albums[albums["Album"] == album]
        if len(listing.Cover.values) > 0:
            file_name = str(listing.Cover.values[0])
            return join(self.path, artist, album, file_name)
        else:
            return ""

    def get_random_album(self):
        """ Return a randomly selected artist and album. """
        row = self.data_frame.sample()
        return row.Artist.values[0], row.Album.values[0]

    def get_path(self, artist, album):
        """
        Return the full path to the specified album. If the album does not
        exist, return an empty string.
        """
        path = join(self.path, artist, album)
        return path if exists(path) else ""

    def get_tracks(self, artist, album):
        """
        Return a list of the album tracks
        """
        albums = self.data_frame[self.data_frame["Artist"] == artist]
        tracks = albums[albums["Album"] == album]
        return list(tracks.Track)

    def search(self, term):
        """
        Search for all albums which match this term, either in the artist
        name of the album name, then return one on them randomly.

        Returns:
             A dictionary with the keys "artist", "album" and "path" as keys
             if found. Return an empty dictionary otherwise.
        """
        df = self.data_frame
        term = term.lower()
        results = df[(df["Album"].str.lower().str.find(term) > -1) |
                     (df["Artist"].str.lower().str.find(term) > -1)]

        if results.empty:
            return {}
        else:
            row = results.sample()
            artist = row.Artist.values[0]
            album = row.Album.values[0]
            return {"artist": artist,
                    "album": album,
                    "path": self.get_path(artist, album)}
