"""This module handle the ZenKeyPy Controller."""

from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime
from logging import getLogger

from mpd import MPDClient
from pynput.keyboard import Listener
from requests import get

logger = getLogger(__name__)


@contextmanager
def get_mdp_client() -> Generator[MPDClient, None, None]:
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        yield client

    finally:
        try:
            client.close()
            client.disconnect()
        except Exception as e:  # noqa: BLE001
            logger.error("Error unloading MDPClient: %s", e)


class ZenMPD:
    _paused = 0

    @staticmethod
    def play():
        with get_mdp_client() as client:
            status = client.status()
            if status.get("state") == "pause":
                client.pause(0)
            elif status.get("state") != "play":
                client.play(int(status.get("song", 0)))
        ZenMPD._paused = 1

    @staticmethod
    def pause():
        with get_mdp_client() as client:
            ZenMPD._paused = 1 - ZenMPD._paused
            client.pause(ZenMPD._paused)

    @staticmethod
    def stop():
        with get_mdp_client() as client:
            client.stop()
        ZenMPD._paused = 0

    @staticmethod
    def previous():
        with get_mdp_client() as client:
            pos = int(client.status().get("song", 0))
            client.play(max(pos - 1, 0))
        ZenMPD._paused = 0

    @staticmethod
    def next():
        with get_mdp_client() as client:
            status = client.status()
            pos = int(status.get("song", -1))
            if pos + 1 < int(status.get("playlistlength", 0)):
                client.play(pos + 1)
        ZenMPD._paused = 0

    @staticmethod
    def volup():
        with get_mdp_client() as client:
            status = client.status()
            volume = int(status.get("volume", 0))
            client.setvol(min(volume + 5, 100))

    @staticmethod
    def voldown():
        with get_mdp_client() as client:
            status = client.status()
            volume = int(status.get("volume", 0))
            client.setvol(max(volume - 5, 0))


class Controller:
    """This class serves as the main delegator for Hotkey actions."""

    listener: Listener | None = None

    messages: list | None = None
    """A list of messages received for the Controller."""

    def __init__(self: "Controller", zenplayer_url: str) -> None:
        """Construct the Controller object."""
        self.zen_player_url = zenplayer_url
        if Controller.messages is None:
            Controller.messages = []

    @staticmethod
    def _add_message(msg: str) -> None:
        """Add the specified message to the messages list."""
        message = f"{datetime.now().isoformat()}: {msg}"
        logger.debug(message)
        Controller.messages.append(message)

    def zenplayer(self: "Controller", action: str) -> None:
        """Call the specified ZenPlayer function."""
        resp = get(f"{self.zen_player_url}/zenplayer/{action}")
        self._add_message(
            f"ZenPlayer called: {action} = {resp.status_code}. {resp.json()}"
        )

    def zenmpd(self: "Controller", action: str) -> None:
        """Call the specified ZenPlayer function."""
        resp = getattr(ZenMPD, action)()
        self._add_message(f"ZenMPD called: {action} - {resp}")

    def controller(self: "Controller", action: str) -> None:
        """Call the specified Controller function."""
        if self.listener is None:
            self._add_message("Signal to quit but no listener set.")
        else:
            self._add_message("Signal to quit")
            self.listener.stop()
