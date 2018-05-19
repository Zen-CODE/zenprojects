"""
ZenSync
=======

This module provides simple backup/sync functionality
"""
import os
from os.path import isdir, join


path = r"./"


def process_folder(folder):
    for file_name in os.listdir(folder):
        full_name = join(folder, file_name)
        if isdir(full_name):
            process_folder(full_name)
        else:
            print("Got file {0}".format(full_name))


class UI(object):
    """
    Handles the presentation
    """
    @staticmethod
    def show_splash():
        print("\n".join(["=" * 11, "= ZenSync =", "=" * 11, "\n"]))


if __name__ == "__main__":
    UI.show_splash()
    process_folder(path)
