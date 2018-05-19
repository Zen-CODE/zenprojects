"""
ZenSync
=======

This module provides simple backup/sync functionality
"""
import os
from os.path import isdir, join, abspath, exists


class SyncHandler(object):
    """
    Handles the synchronization task between two given folders.
    """
    # TODO: Implement
    replace = False
    """ Always replace files in the destination. """

    # TODO: Implement
    clean = False
    """ Remove files that are not in the source folder """

    def sync_folder(self, source, dest):
        """
        Synchronizes the contents of the sources and destination folder.
        """
        for file_name in os.listdir(source):
            full_name = join(source, file_name)
            if isdir(full_name):
                UI.show_message("Processing sub-folder: {0}".format(full_name))
                self.sync_folder(full_name, join(dest, file_name))
            else:
                full_dest = join(dest, file_name)
                UI.show_message("Got file {0}".format(full_name))
                if exists(full_dest):
                    UI.show_message("file exists")
                else:
                    UI.show_message("file does not exists")


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
    path = r"./"
    dest = "/home/richard/Temp/"

    UI.show_splash()
    sync = SyncHandler()
    sync.sync_folder(abspath(path), dest)
