"""This module handle the ZenKeyPy Controller."""
from pynput.keyboard import Listener

from requests import get


class Controller:
    """This class serves as the main delegator for Hotkey actions."""

    listener: Listener = None

    def __init__(self: 'Controller', zenplayer_url: str) -> None:
        """Construct the Controller object."""
        self.zen_player_url = zenplayer_url

    def zenplayer(self: 'Controller', action: str) -> None:
        """Call the specified ZenPlayer function."""
        resp = get("/".join([self.zen_player_url, "zenplayer", action]))
        print(f"ZenPlayer called: {action}, response {resp.status_code}")  # noqa T001

    def controller(self: 'Controller', action: str) -> None:
        """Call the specified Controller function."""
        # Signal a quit on any call to the controller
        print(f"Signal to quit")  # noqa T001
        if self.listener is None:
            print(f"Listener is none. Please set before quitting.")  # noqa T001
        else:
            self.listener.stop()
