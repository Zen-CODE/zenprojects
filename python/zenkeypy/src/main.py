"""This module houses the entrypoint for ZenKeyPy."""
from controller import Controller

from hotkey_handler import HotKeyHandler


if __name__ == "__main__":
    print("Launching ZenKeyPy...")  # noqa T001
    ctrl = Controller()
    listener = HotKeyHandler.add_bindings(ctrl)
    listener.join()
