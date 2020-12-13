"""This module houses the entrypoint for ZenKeyPy."""
from config import Config

from controller import Controller

from hotkey_handler import HotKeyHandler


if __name__ == "__main__":
    print("Launching ZenKeyPy...")  # noqa T001
    config = Config.get_config()
    ctrl = Controller(config["zenplayer_url"])
    listener = HotKeyHandler.create_bindings(
        config["hotkeymap"], ctrl)
    ctrl.listener = listener
    listener.join()
