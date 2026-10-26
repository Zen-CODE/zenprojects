"""This module handle the ZenKeyPy Controller."""

from logging import getLogger
from threading import Timer

from pynput.keyboard import Listener
from requests import get

from zenmpd import ZenMPD

logger = getLogger(__name__)



class Controller:
    """This class serves as the main delegator for Hotkey actions."""

    listener: Listener | None = None
    timer: Timer | None = None

    def __init__(self: "Controller", zenplayer_url: str) -> None:
        """Construct the Controller object."""
        self.zen_player_url = zenplayer_url
        ZenMPD.connect_client()

        if not Controller.timer:
            Controller.set_timer()

    @staticmethod
    def set_timer():
        Controller.timer = Timer(1, Controller.timed_event)
        Controller.timer.start()

    @staticmethod
    def timed_event():
        if ZenMPD.client:
            state = ZenMPD.status()
            if state.get("state") == "stop":
                logger.info("MPD is stopped, playing a random album.")
                ZenMPD.playrandomalbum()
            else:
                logger.info(f"MPD is playing \tElapsed: {state.get("elapsed", "")}")

            Controller.set_timer()
        else:
            logger.warning("Timer event: MPD client is not connected.")

    def zenplayer(self: "Controller", action: str) -> None:
        """Call the specified ZenPlayer function."""
        resp = get(f"{self.zen_player_url}/zenplayer/{action}")
        logger.info(
            f"ZenPlayer called: {action} = {resp.status_code}. {resp.json()}"
        )

    def zenmpd(self: "Controller", action: str) -> None:
        """Call the specified ZenPlayer function."""
        resp = getattr(ZenMPD, action)()
        if resp:
            keys = ["volume", "state", "file", "bitrate", "elapsed", "duration"]
            details = [f"  {k.title()}: {v}" for k, v in resp.items() if k in keys]
            logger.info(f"ZenMPD called: {action}:\n" + "\n".join(details))
        else:
            logger.info(f"ZenMPD called: {action}")

    def controller(self: "Controller", action: str) -> None:
        """Call the specified Controller function."""
        logger.info("ZenMPD called: Exiting")
        ZenMPD.disconnect_client()
        self.timer.cancel()
        self.listener.stop()
