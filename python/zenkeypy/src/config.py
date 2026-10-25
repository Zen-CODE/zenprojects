"""This module houses the ZenKeyPy configuration dictionary creator."""

from json import load


class Config:
    """This class is loads and provides the ZenKeyPy configuration dict."""

    _config: dict | None = None

    @staticmethod
    def get_config() -> dict:
        """Return the ZenKeyPy configuration dictionary."""
        if Config._config is None:
            with open("hotkeys.json") as f:
                Config._config = load(f)
        return Config._config
