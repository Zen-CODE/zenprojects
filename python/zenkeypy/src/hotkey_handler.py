"""This module adds global hotkey support from ZenPlayer."""
from functools import partial
from typing import Dict

from controller import Controller


from pynput.keyboard import GlobalHotKeys


class HotKeyHandler:
    """This class add global hotkey for calling ZenPlayer funtions.

    Hotkey bindings are set via the `hotkey.json` file in this folder.
    """

    @staticmethod
    def create_bindings(mapping: Dict, ctrl: Controller) -> GlobalHotKeys:
        """Create hotkey bindings from the mapping to the controller actions.

        Args:
            mapping a dictionary with the key as the hotkey combination and the
            value as the controller action.
        """
        mapdict = {
            k: partial(ctrl.zenplayer, v) for k, v in mapping.items()}
        ghk = GlobalHotKeys(mapdict)
        ghk.start()
        return ghk
