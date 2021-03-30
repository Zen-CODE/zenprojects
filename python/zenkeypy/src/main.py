"""This module houses the entrypoint for ZenKeyPy."""
from config import Config
from typing import Dict

from fastapi import FastAPI

from controller import Controller

from hotkey_handler import HotKeyHandler

app = FastAPI()


class ZenKeyApp():
    """This class houses the ZenKeyPy API interface."""

    _ctrl: Controller = None

    @staticmethod
    def start() -> None:
        """Create and bind a properly configured ZenKeyApp instance."""
        config = Config.get_config()
        ZenKeyApp._ctrl = ctrl = Controller(config["zenplayer_url"])
        listener = HotKeyHandler.create_bindings(
            config["hotkeymap"], ctrl)
        ctrl.listener = listener
        '''
        If we want to wait and block for messages:
            listener.join()
        '''

    @staticmethod
    @app.get("/")
    def read_root() -> Dict:
        """Return the root of out API."""
        return {"Hello": "zen"}

    @staticmethod
    @app.get("/history/")
    def history() -> Dict:
        """Return the list of actions in our history."""
        return {"items": ZenKeyApp._ctrl.messages}


ZenKeyApp.start()
