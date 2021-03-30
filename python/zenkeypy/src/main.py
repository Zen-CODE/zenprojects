"""This module houses the entrypoint for ZenKeyPy."""
from config import Config
from typing import Dict

from fastapi import FastAPI

from controller import Controller

from hotkey_handler import HotKeyHandler

app = FastAPI()


class ZenKeyApp():
    """This class houses the ZenKeyPy API interface."""

    @staticmethod
    def get_controller(wait: bool = False) -> Controller:
        """Build and return a properly configured ZenKeyApp instance."""
        config = Config.get_config()
        ctrl = Controller(config["zenplayer_url"])
        listener = HotKeyHandler.create_bindings(
            config["hotkeymap"], ctrl)
        ctrl.listener = listener
        if wait:
            print("ZenKeyApp - joining threads")
            listener.join()

        print("ZenKeyApp - returning controller.")
        return ctrl

    @staticmethod
    @app.get("/")
    def read_root() -> Dict:
        """Return the root of out API."""
        return {"Hello": "zen"}

    @staticmethod
    @app.get("history/")
    def history() -> Dict:
        """Return the list of actions in our history."""
        return {"items": []}


ctrl = ZenKeyApp.get_controller()
