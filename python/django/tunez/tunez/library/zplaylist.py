""" This modules houses the wrapper around the ZenPLaylist """
from os import environ
from requests import get


class ZPlaylist:
    """
    Houses the class that interfaces with the ZenPlaylist component.
    """
    def __init__(self):
        super().__init__()
        self.address = environ["ZP_URL"]
        """ The URL of the ZenPlayer endpoint """

    def folder_add(self, **kwargs):
        """ Add the specified folder to the playlist """
        resp = get(self.address + "/zenplaylist/add_files",
                   params=kwargs)
        return resp.json()
