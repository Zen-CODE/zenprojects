"""This module adds global hotkey support from ZenPlayer."""
from json import load
from typing import Dict

from controller import Controller

from pynput.keyboard import GlobalHotKeys


class HotKeyHandler:
    """This class add global hotkey for calling ZenPlayer funtions.

    Hotkey bindings are set via the `hotkey.json` file in this folder.
    """

    @staticmethod
    def add_bindings(ctrl: Controller) -> None:
        """Add the specified keybinding to action on the given controller."""
        mapping = HotKeyHandler._load_hotkeymap()
        return HotKeyHandler._create_bindings(mapping, ctrl)

    @staticmethod
    def _load_hotkeymap() -> Dict:
        """Return the specified hotkey mappingsloaded from the json file."""
        with open("src/hotkeys.json") as f:
            mappings = load(f)
        return mappings["hotkeymap"]

    @staticmethod
    def _create_bindings(mapping: Dict, ctrl: Controller) -> GlobalHotKeys:
        """
        Create hotkey bindings from the mapping to the controller actions.

        Args:
            mapping a dictionary with the key as the hotkey combination and the
            value as the controller action.
        """
        mapdict = {
            k: getattr(ctrl, v) for k, v in mapping.items()}
        ghk = GlobalHotKeys(mapdict)
        ghk.start()
        return ghk
