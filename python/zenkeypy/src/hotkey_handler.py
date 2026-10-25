"""This module adds global hotkey support from ZenPlayer."""

from functools import partial

from pynput.keyboard import GlobalHotKeys

from controller import Controller


class HotKeyHandler:
    """This class add global hotkey for calling ZenPlayer functions.

    Hotkey bindings are set via the `hotkey.json` file in this folder.
    """

    @staticmethod
    def create_bindings(mapping: dict, ctrl: Controller) -> GlobalHotKeys:
        """Create hotkey bindings from the mapping to the controller actions.

        Args:
            mapping a dictionary with the key as the hotkey combination and the
            value as the controller action.
        """
        mapdict = {}
        for k, v in mapping.items():
            mapdict[k] = partial(getattr(ctrl, v["function"]), *v["params"])
        ghk = GlobalHotKeys(mapdict)
        ghk.start()
        return ghk
