"""This module houses the entrypoint for ZenKeyPy."""
from requests.api import get
from config import Config
from typing import Dict
from sys import argv
from logging import basicConfig, DEBUG, getLogger, INFO
import sys
from fastapi import FastAPI
from controller import Controller
from hotkey_handler import HotKeyHandler

basicConfig(stream=sys.stdout, level=DEBUG)
app = FastAPI()
logger = getLogger(__name__)


class ZenKeyApp():
    """This class houses the ZenKeyPy API interface."""

    _ctrl: Controller = None

    @staticmethod
    def start(wait=False) -> None:
        """Create and bind a properly configured ZenKeyApp instance."""
        config = Config.get_config()
        ZenKeyApp._ctrl = ctrl = Controller(config["zenplayer_url"])
        listener = HotKeyHandler.create_bindings(
            config["hotkeymap"], ctrl)
        ctrl.listener = listener

        if wait:
            listener.join()

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


if len(argv) > 1 and argv[1] == "basic":
    logger.info("Launching ZenKeyPy without FastAPI interface...")
    ZenKeyApp.start(True)
else:
    logger.info("Launching ZenKeyPy...")
    ZenKeyApp.start()
