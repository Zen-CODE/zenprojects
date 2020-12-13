"""This module houses the entrypoint for ZenKeyPy."""
from hotkey_handler import HotKeyHandler


class Controller:
    """This class serves as the main delegator for Hotkey actions."""

    def play_pause(self: 'Controller') -> None:
        """Play or pause the current media."""
        print("play plause fired")  # noqa T001


if __name__ == "__main__":
    print("Launching ZenKeyPy...")  # noqa T001
    ctrl = Controller()
    listener = HotKeyHandler.add_bindings(ctrl)
    listener.join()
