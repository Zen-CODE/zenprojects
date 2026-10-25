"""This module handle the ZenKeyPy Controller."""

from collections.abc import Generator
from contextlib import contextmanager
from logging import getLogger
from os import listdir
from pathlib import Path
from random import choice

from mpd import MPDClient
from pynput.keyboard import Listener
from requests import get

MUSIC_DIR = "/home/richard/Zen/Music/"

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
    def _get_library_files(folder: str, existing: list | None = None) -> list[str]:
        top_level = bool(existing is None)
        files = [] if top_level else existing
        for f in sorted(listdir(folder), reverse=False):
            file_path = Path(f"{folder}/{f}")
            if file_path.is_dir():
                ZenMPD._get_library_files(str(file_path), existing=files)
            else:
                ext = f.split(".")[-1].lower()
                if ext in ["mp3", "flac", "wav", "m4a"]:
                    files.append(str(file_path))
        return [fname.replace(MUSIC_DIR, "") for fname in files]

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


    @staticmethod
    def _choose_random_album(client: MPDClient) -> str | None:
        all_files = client.listall("/")
        chosen, count = None, 0
        while count < 100 and not chosen:
            candidate = choice(all_files)
            if file_name := candidate.get("file"):
                chosen = file_name.split("/", maxsplit=2)
                chosen = "/".join(chosen[0:2])
            count += 1
        return f"{MUSIC_DIR}{chosen}"

    @staticmethod
    def playrandomalbum():
        with get_mdp_client() as client:
            if chosen := ZenMPD._choose_random_album(client):
                client.clear()
                for file_ in ZenMPD._get_library_files(chosen):
                    client.add(file_)
                client.play(0)

    @staticmethod
    def nowplaying() -> dict:
        with get_mdp_client() as client:
            status: dict = client.status()
            song: dict = client.currentsong()

        return status | song

class Controller:
    """This class serves as the main delegator for Hotkey actions."""

    listener: Listener | None = None

    def __init__(self: "Controller", zenplayer_url: str) -> None:
        """Construct the Controller object."""
        self.zen_player_url = zenplayer_url

    def zenplayer(self: "Controller", action: str) -> None:
        """Call the specified ZenPlayer function."""
        resp = get(f"{self.zen_player_url}/zenplayer/{action}")
        logger.info(
            f"ZenPlayer called: {action} = {resp.status_code}. {resp.json()}"
        )

    def zenmpd(self: "Controller", action: str) -> None:
        """Call the specified ZenPlayer function."""
        resp = getattr(ZenMPD, action)()
        if resp:
            keys = ["volume", "state", "file", "bitrate", "elapsed", "duration"]
            details = [f"  {k.title()}: {v}" for k, v in resp.items() if k in keys]
            logger.info(f"ZenMPD called: {action}:\n" + "\n".join(details))
        else:
            logger.info(f"ZenMPD called: {action}")

    def controller(self: "Controller", action: str) -> None:
        """Call the specified Controller function."""
        logger.info("ZenMPD called: Exiting")
        self.listener.stop()
