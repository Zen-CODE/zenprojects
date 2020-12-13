"""This module adds global hotkey support from ZenPlayer."""
from typing import Dict
from functools import partial

from controller import Controller
from config import Config

from pynput.keyboard import GlobalHotKeys


class HotKeyHandler:
    """This class add global hotkey for calling ZenPlayer funtions.

    Hotkey bindings are set via the `hotkey.json` file in this folder.
    """

    @staticmethod
    def add_bindings(ctrl: Controller) -> None:
        """Add the specified keybinding to action on the given controller."""
        mapping = Config.get_config()["hotkeymap"]
        return HotKeyHandler._create_bindings(mapping, ctrl)

    @staticmethod
    def _create_bindings(mapping: Dict, ctrl: Controller) -> GlobalHotKeys:
        """
        Create hotkey bindings from the mapping to the controller actions.

        Args:
            mapping a dictionary with the key as the hotkey combination and the
            value as the controller action.
        """
        mapdict = {
            k: partial(ctrl.zenplayer, v) for k, v in mapping.items()}
        ghk = GlobalHotKeys(mapdict)
        ghk.start()
        return ghk
