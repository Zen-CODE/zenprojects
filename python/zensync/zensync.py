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
            clean_folder(full_name)
        else:
            print("Got file {0}".format(full_name))


process_folder(path)
print("Starting sync...")
