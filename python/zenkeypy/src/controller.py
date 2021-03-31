"""This module handle the ZenKeyPy Controller."""
from typing import List
from pynput.keyboard import Listener
from datetime import datetime

from requests import get


class Controller:
    """This class serves as the main delegator for Hotkey actions."""

    listener: Listener = None

    messages: List = []
    """A list of messages received for the Controller."""

    def __init__(self: 'Controller', zenplayer_url: str) -> None:
        """Construct the Controller object."""
        self.zen_player_url = zenplayer_url

    @staticmethod
    def _add_message(msg: str) -> None:
        """Add the specified message to the messages list."""
        Controller.messages.append(f'{datetime.now().isoformat()}: {msg}')

    def zenplayer(self: 'Controller', action: str) -> None:
        """Call the specified ZenPlayer function."""
        resp = get("/".join([self.zen_player_url, "zenplayer", action]))
        self._add_message(
            f"ZenPlayer called: {action} = {resp.status_code}. {resp.content}")

    def controller(self: 'Controller', action: str) -> None:
        """Call the specified Controller function."""
        if self.listener is None:
            self._add_message("Signal to quit but no listener set.")
        else:
            self._add_message("Signal to quit")
            self.listener.stop()
