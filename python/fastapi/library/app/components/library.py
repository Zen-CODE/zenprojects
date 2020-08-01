from os.path import join, isdir, basename, expanduser
from random import sample
from glob import glob
from random import choice
from .filesystemextractor import FileSystemExtractor as fse
import pandas as pd



class Library:
    """
    Class for fetching information about our music library. This information
    is contained entirely in the folder names and structures.

    Args:
        path (str): The path to the roo music library folder.
    """

    def __init__(self, path="~/Music"):
        self.path = path = expanduser(path)
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

    # def get_random_artists(self, number):
    #     """ Return a random list of *number* artists. """
    #     artists = self.get_artists()
    #     return sample(artists, number)

    # def get_random_albums(self, artist, number):
    #     """ Return a random list of *number* albums by *artist*. """
    #     albums = self.get_albums(artist)
    #     if albums:
    #         return sample(albums, number)
    #     else:
    #         raise (Exception("No albums found for {0}".format(artist)))

    # def get_albums(self, artist):
    #     """ Return a list of albums for the *artist*. """
    #     return sorted(self._artists.get(artist, []))

    # def get_album_cover(self, artist, album):
    #     """
    #     Return the full path to the album cover for the specified album or the
    #     default library image one does not exist.
    #     """
    #     path = join(self.path, artist, album)
    #     pattern = "cover.*"
    #     matches = glob(join(path, pattern))
    #     return matches[0] if matches else join(self.path, "default.png")

    # def get_path(self, artist, album):
    #     """ Return the full path to the specified album. """
    #     return join(self.path, artist, album)

    # def get_random_album(self):
    #     """
    #     Return the artist and album of a random album as an artist, album tuple
    #     """
    #     return choice(self._albums)

    # @staticmethod
    # def _get_any_matches(path, *exts):
    #     """ Return the first valid files matching the extensions
    #     in the path specified."""
    #     for ext in exts:
    #         matches = glob(join(path, ext))
    #         if matches:
    #             return matches
    #     return None

    # def get_tracks(self, artist, album):
    #     """
    #     Return a list of the album tracks
    #     """

    #     def get_name(fname):
    #         """"Return the nice, cleaned name of the track"""
    #         return basename(fname)  # [:-4]

    #     path = join(self.path, artist, album)
    #     matches = self._get_any_matches(
    #         path, "*.mp3", "*.ogg", "*.m4a", "*.wma")
    #     if matches:
    #         return sorted([get_name(f) for f in matches])
    #     else:
    #         return []

    # def search(self, term):
    #     """
    #     Search for all albums which match this term, either in the artist
    #     name of the album name, then return one on them randomly.

    #     Returns:
    #          A dictionary with the keys "artist", "album" and "path" as keys
    #          if found. Return an empty dictionary otherwise.
    #     """
    #     terms = term.lower().split(" ")
    #     matches = []
    #     for artist in self._artists.keys():
    #         for album in self._artists[artist]:
    #             if all([(artist + album).lower().find(t) > -1
    #                     for t in terms]):
    #                 matches.append(
    #                     {"artist": artist,
    #                      "album": album,
    #                      "path": self.get_path(artist, album)})
    #     return choice(matches) if matches else []
