from os import listdir
from pathlib import Path
from random import choice

from mpd import MPDClient

MUSIC_DIR = "/home/richard/Zen/Music/"


class ZenMPD:
    _paused = 0

    client: MPDClient | None = None

    @staticmethod
    def connect_client():
        """Initialise the connected client"""
        if ZenMPD.client is None:
            ZenMPD.client = MPDClient()
            ZenMPD.client.connect("localhost", 6600)

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
        status = ZenMPD.client.status()
        if status.get("state") == "pause":
            ZenMPD.client.pause(0)
        elif status.get("state") != "play":
            ZenMPD.client.play(int(status.get("song", 0)))
        ZenMPD._paused = 1

    @staticmethod
    def pause():
        ZenMPD._paused = 1 - ZenMPD._paused
        ZenMPD.client.pause(ZenMPD._paused)

    @staticmethod
    def stop():
        ZenMPD.client.stop()
        ZenMPD._paused = 0

    @staticmethod
    def previous():
        pos = int(ZenMPD.client.status().get("song", 0))
        ZenMPD.client.play(max(pos - 1, 0))
        ZenMPD._paused = 0

    @staticmethod
    def next():
        status = ZenMPD.client.status()
        pos = int(status.get("song", -1))
        if pos + 1 < int(status.get("playlistlength", 0)):
            ZenMPD.client.play(pos + 1)
        ZenMPD._paused = 0

    @staticmethod
    def volup():
        status = ZenMPD.client.status()
        volume = int(status.get("volume", 0))
        ZenMPD.client.setvol(min(volume + 5, 100))

    @staticmethod
    def voldown():
        status = ZenMPD.client.status()
        volume = int(status.get("volume", 0))
        ZenMPD.client.setvol(max(volume - 5, 0))


    @staticmethod
    def _choose_random_album(client: MPDClient) -> str | None:
        all_files = ZenMPD.client.listall("/")
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
        if chosen := ZenMPD._choose_random_album(ZenMPD.client):
            ZenMPD.client.clear()
            for file_ in ZenMPD._get_library_files(chosen):
                ZenMPD.client.add(file_)
            ZenMPD.client.play(0)

    @staticmethod
    def nowplaying() -> dict:
        status: dict = ZenMPD.client.status()
        song: dict = ZenMPD.client.currentsong()
        return status | song

    @staticmethod
    def status() -> dict:
        return ZenMPD.client.status()

    @staticmethod
    def disconnect_client():
        """Initialise the connected client"""
        if ZenMPD.client is not None:
            ZenMPD.client.close()
            ZenMPD.client.disconnect()
            ZenMPD.client = None

