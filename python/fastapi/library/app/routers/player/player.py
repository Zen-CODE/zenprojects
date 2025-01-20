
from requests import get


ZENPLAYER_URL = "http://127.0.0.1:9001/"


class ZenPlayerController:
    """
    This class provides an interface from controlling the active ZenPlayer
    instance.
    """

    @staticmethod
    def get_state():
        """Return the state of the current ZenPlayer instance."""
        response = get(ZENPLAYER_URL + "/zenplayer/get_state")
        return response.json()
