"""This module handle the ZenKeyPy Controller."""
from typing import List
from pynput.keyboard import Listener

from requests import get


class Controller:
    """This class serves as the main delegator for Hotkey actions."""

    listener: Listener = None

    messages: List = []
    """A list of messages received for the Controller."""

    def __init__(self: 'Controller', zenplayer_url: str) -> None:
        """Construct the Controller object."""
        self.zen_player_url = zenplayer_url

    def zenplayer(self: 'Controller', action: str) -> None:
        """Call the specified ZenPlayer function."""
        resp = get("/".join([self.zen_player_url, "zenplayer", action]))
        Controller.messages.append(
            f"ZenPlayer called: {action}, response {resp.status_code}")

    def controller(self: 'Controller', action: str) -> None:
        """Call the specified Controller function."""
        if self.listener is None:
            Controller.messages.append("Signal to quit but no listener set.")
        else:
            Controller.messages.append("Signal to quit")
            self.listener.stop()
