"""This module houses the entrypoint for ZenKeyPy."""

import sys
from logging import DEBUG, basicConfig, getLogger
from sys import argv

from fastapi import FastAPI

from config import Config
from controller import Controller
from hotkey_handler import HotKeyHandler


basicConfig(stream=sys.stdout, level=DEBUG)
app = FastAPI()
logger = getLogger(__name__)


class ZenKeyApp:
    """This class houses the ZenKeyPy API interface."""

    _ctrl: Controller = None

    @staticmethod
    def start(wait=False) -> None:
        """Create and bind a properly configured ZenKeyApp instance."""
        config = Config.get_config()
        ZenKeyApp._ctrl = ctrl = Controller(config["zenplayer_url"])
        listener = HotKeyHandler.create_bindings(config["hotkeymap"], ctrl)
        ctrl.listener = listener

        if wait:
            listener.join()

    @staticmethod
    @app.get("/")
    def read_root() -> dict:
        """Return the root of out API."""
        return {"Hello": "zen"}

    @staticmethod
    @app.get("/history/")
    def history() -> dict:
        """Return the list of actions in our history."""
        return {"items": ZenKeyApp._ctrl.messages}


if len(argv) > 1 and argv[1] == "basic":
    logger.info("Launching ZenKeyPy without FastAPI interface...")
    ZenKeyApp.start(True)
else:
    logger.info("Launching ZenKeyPy...")
    ZenKeyApp.start()
