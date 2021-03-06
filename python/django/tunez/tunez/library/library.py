from os import listdir
from os.path import join, isdir, basename, exists
from random import sample
from glob import glob
from random import choice


class MusicLib(object):
    """
    Class for fetching information about our music library. This information
    is contained entirely in the folder names and structures.
    """

    def __init__(self, path):
        self.path = path
        dirs = [name for name in listdir(self.path) if
                isdir(join(self.path, name))]
        artists = {}
        albums = []
        for artist in dirs:
            artists[artist] = []
            artist_path = join(self.path, artist)
            for album in listdir(artist_path):
                if isdir(join(artist_path, album)):
                    artists[artist].append(album)
                    albums.append((artist, album))

        self._artists = artists
        """ A dictionary of lists, where the key is the artist and the value
        the albums.
        """
        self._albums = albums
        """ A list of (artist, album) tuples. We store this only so we can find
        random albums all with an equal chance. The previous algorithm found a
        random artist, then a random album, favouring albums by artists with
        fewer albums.
        """

    def get_artists(self):
        """ Return a list of artists. """
        return list(self._artists.keys())
        # ============ Pure file implementation
        # return [name for name in listdir(self.path) if
        #         isdir(join(self.path, name))]

    def get_random_artists(self, number):
        """ Return a random list of *number* artists. """
        artists = self.get_artists()
        return sample(artists, number)

    def get_random_albums(self, artist, number):
        """ Return a random list of *number* albums by *artist*. """
        albums = self.get_albums(artist)
        if albums:
            return sample(albums, number)
        else:
            raise (Exception("No albums found for {0}".format(artist)))

    def get_albums(self, artist):
        """ Return a list of albums for the *artist*. """
        return self._artists.get(artist, [])
        # ============ Pure file implementation
        # path = join(self.path, artist)
        # if exists(path):
        #     return [name for name in listdir(path) if isdir(join(path, name))]
        # else:
        #     return []

    def get_cover(self, artist, album):
        """
        Return the album cover for the specified album or the default library
        image one does not exist.
        """
        path = join(self.path, artist, album)
        pattern = "cover.*"
        matches = glob(join(path, pattern))
        return matches[0] if matches else join(self.path, "default.png")

    def get_album_path(self, artist, album):
        """ Return the full path to the specified album. """
        return join(self.path, artist, album)

    def get_random_album(self):
        """ Return the artist and album of a random album """
        return choice(self._albums)

    @staticmethod
    def _get_any_matches(path, *exts):
        """ Return the first valid files matching the extensions
        in the path specified."""
        for ext in exts:
            matches = glob(join(path, ext))
            if matches:
                return matches
        return None

    def get_tracks(self, artist, album):
        """
        Return a list of the album tracks
        """

        def get_name(fname):
            """"Return the nice, cleaned name of the track"""
            return basename(fname)  # [:-4]

        path = join(self.path, artist, album)
        matches = self._get_any_matches(
            path, "*.mp3", "*.ogg", "*.m4a", "*.wma")
        if matches:
            return sorted([get_name(f) for f in matches])
        else:
            return []

    def search(self, term):
        """
        Search for all albums which match this term, either in the artist
        name of the album name, then return one on them randomly.

        Returns:
             A dictionary with the artist and album as keys if found. Return an
             empty dictionary otherwise.
        """
        terms = term.lower().split(" ")
        matches = []
        # ============ Pure file implementation
        # for artist in listdir(self.path):
        #     folder = join(self.path, artist)
        #     if isdir(folder):
        #         for album in listdir(folder):
        #             if all([(artist + album).lower().find(t) > -1
        #                     for t in terms]):
        #                 matches.append({"artist": artist, "album": album})
        for artist in self._artists.keys():
            for album in self._artists[artist]:
                if all([(artist + album).lower().find(t) > -1
                        for t in terms]):
                    matches.append({"artist": artist, "album": album})
        return choice(matches) if matches else []
