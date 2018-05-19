"""
ZenSync
=======

This module provides simple backup/sync functionality
"""
import os
from os.path import isdir, join, abspath


path = r"./"
dest = "/home/richard/Temp/"


class SyncHandler(object):
    """
    Handles the synchronization task between two given folders.
    """

    def sync_folder(self, source, dest):
        for file_name in os.listdir(source):
            full_name = join(source, file_name)
            if isdir(full_name):
                self.sync_folder(full_name)
            else:
                UI.show_message("Got file {0}".format(full_name))


class UI(object):
    """
    Handles the presentation
    """
    @staticmethod
    def show_splash():
        print("\n".join(["=" * 11, "= ZenSync =", "=" * 11, "\n"]))

    @staticmethod
    def show_message(msg):
        """ Display a message during processing. """
        print(msg)


if __name__ == "__main__":
    UI.show_splash()
    sync = SyncHandler()
    sync.sync_folder(abspath(path), dest)
