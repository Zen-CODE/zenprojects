"""This module handle the ZenKeyPy Controller."""

from pynput.keyboard import Listener
from requests import get

from zenmpd import ZenMPD


class Controller:
    """This class serves as the main delegator for Hotkey actions."""

    listener: Listener | None = None

    def __init__(self: "Controller", zenplayer_url: str) -> None:
        """Construct the Controller object."""
        self.zen_player_url = zenplayer_url
        ZenMPD.connect_client()

    def zenplayer(self: "Controller", action: str) -> None:
        """Call the specified ZenPlayer function."""
        resp = get(f"{self.zen_player_url}/zenplayer/{action}")
        print(
            f"ZenPlayer called: {action} = {resp.status_code}. {resp.json()}"
        )

    def zenmpd(self: "Controller", action: str) -> None:
        """Call the specified ZenPlayer function."""
        resp = getattr(ZenMPD, action)()
        if resp:
            keys = ["volume", "state", "file", "bitrate", "elapsed", "duration"]
            details = [f"  {k.title()}: {v}" for k, v in resp.items() if k in keys]
            print(f"ZenMPD called: {action}:\n" + "\n".join(details))
        else:
            print(f"ZenMPD called: {action}")

    def controller(self: "Controller", action: str) -> None:
        """Call the specified Controller function."""
        ZenMPD.disconnect_client()
        self.listener.stop()
