"""This module handle the ZenKeyPy Controller."""
from requests import get


class Controller:
    """This class serves as the main delegator for Hotkey actions."""

    def __init__(self: 'Controller') -> None:
        """Contruct the Controller object."""
        self.zen_player_url = "http://0.0.0.0:9001"

    def play_pause(self: 'Controller') -> None:
        """Play or pause the current media."""
        get("/".join([self.zen_player_url, "zenplayer", "play_pause"]))
        print("play plause fired")  # noqa T001
