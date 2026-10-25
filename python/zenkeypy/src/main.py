"""This module houses the entrypoint for ZenKeyPy."""

import sys
from logging import INFO, basicConfig, getLogger

from config import Config
from controller import Controller
from hotkey_handler import HotKeyHandler

basicConfig(stream=sys.stdout, level=INFO)
logger = getLogger(__name__)


class ZenKeyApp:
    """This class houses the ZenKeyPy API interface."""

    _ctrl: Controller = None

    @staticmethod
    def start() -> None:
        """Create and bind a properly configured ZenKeyApp instance."""
        config = Config.get_config()
        ZenKeyApp._ctrl = ctrl = Controller(config["zenplayer_url"])
        listener = HotKeyHandler.create_bindings(config["hotkeymap"], ctrl)
        ctrl.listener = listener

        listener.join()


if __name__ == "__main__":
    logger.info("Launching ZenKeyP ...")
    ZenKeyApp.start()
