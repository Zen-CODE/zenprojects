"""This module handle the ZenKeyPy Controller."""
from requests import get


class Controller:
    """This class serves as the main delegator for Hotkey actions."""

    def __init__(self: 'Controller') -> None:
        """Contruct the Controller object."""
        self.zen_player_url = "http://0.0.0.0:9001"

    def zenplayer(self: 'Controller', func: str) -> None:
        """Call the specified ZenPlayer function."""
        resp = get("/".join([self.zen_player_url, "zenplayer", func]))
        print(f"ZenPlayer called: {func}, response {resp.status_code}")  # noqa T001
