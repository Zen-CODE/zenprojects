"""
ZenSync
=======

This module provides simple backup/sync functionality
"""
from os import makedirs, listdir, remove
from os.path import isdir, join, abspath, exists, getsize
from shutil import copy
from json import load, dump


class FileSystemOps(object):
    """
    Handle and log all file operation
    """
    follow_symlinks = False

    copied, replaced, removed, skipped = 0, 0, 0, 0

    def copy(self, source, dest):
        """ Copy the source file to the destination. Overwrite if it exists. """
        if exists(dest):
            UI.show_message("Replacing file {0}".format(dest), replace=True)
            self.replaced = self.replaced + 1
        else:
            UI.show_message("Copying to {0}".format(dest), replace=True)
            self.copied = self.copied + 1  # Do not use += 1!
        copy(source, dest, follow_symlinks=self.follow_symlinks)

    def remove(self, dest):
        """ Remove the specified file. """
        UI.show_message(("Removing {0}".format(dest)), replace=True)
        self.removed = self.removed + 1
        remove(dest)

    def skip(self, dest):
        """ Skip processing on the specified file. """
        UI.show_message("Skipping file {0}".format(dest), replace=True)
        self.skipped = self.skipped


class Settings(object):
    """
    Handles the loading and saving of system settings via a json file.
    """
    store_file = '.zensync.json'
    """ The file used to store our settings."""

    @staticmethod
    def load():
        """
        Return a dictionary containing the users previously selected settings
        or te default settings.
        """
        if exists(Settings.store_file):
            with open(Settings.store_file, 'r') as f:
                return load(f)
        else:
            return {}

    @staticmethod
    def save(settings):
        """
        Save the specified dictionary of settings to the store file
        """
        with open(Settings.store_file, 'w') as f:
            dump(settings, f)


class SyncHandler(object):
    """
    Handles the synchronization task between two given folders.
    """
    # TODO: Implement
    replace = False
    """ Always replace files in the destination. """

    # TODO: Implement
    clean = True
    """ Remove files that are not in the source folder """

    # TODO: Implement
    follow_symlinks = False

    def __init__(self):
        self.fso = FileSystemOps()

    @staticmethod
    def file_different(source, dest):
        """
        Return True if the files are different. The default check is for size
        only.
        """
        s_size, d_size = getsize(source), getsize(dest)
        return bool(s_size != d_size)

    def sync_folder(self, source, dest):
        """
        Synchronizes the contents of the sources and destination folder.
        """
        # Note: We use listdir i.s.o. walk to we need tighter control over
        # iteration to maintain the mapping the the destination
        files = listdir(source)
        for item in files:
            f_source, f_dest = join(source, item),  join(dest, item)
            if isdir(f_source):
                self.sync_folder(f_source, f_dest)
            elif not exists(f_dest) or self.file_different(f_source, f_dest):
                if not exists(dest):
                    makedirs(dest)
                self.fso.copy(f_source, f_dest)
            else:
                self.fso.skip(f_dest)

        if self.clean:
            self._clean_dest(files, dest)

    def _clean_dest(self, files, dest):
        """
        Remove files that are in the dest folder and not in the source.

            files: the list of files in that should NOT be removed
        """
        if not exists(dest):
            return
        for item in listdir(dest):
            sub_item = join(dest, item)
            if not isdir(sub_item) and item not in files:
                self.fso.remove(sub_item)


class UI(object):
    """
    Handles the presentation
    """
    last_length = 0

    @staticmethod
    def show_splash():
        print("\n".join(["=" * 11, "= ZenSync =", "=" * 11, "\n"]))

    @staticmethod
    def show_message(msg, replace=False):
        """ Display a message during processing. If Replace is True, the last
        message displayed is replaced.
        """

        if replace:
            print(UI.last_length * chr(8), end='')
        print(msg, end='')
        UI.last_length = len(msg)

    @staticmethod
    def show_summary(settings, fso):
        k = 80  # Length of line
        print("\n".join(["=" * k,
                         "Source   : {0}".format(settings['source']),
                         "Dest     : {0}".format(settings['dest']),
                         "=" * k,
                         "Copied   : {0}".format(fso.copied),
                         "Replaced : {0}".format(fso.replaced),
                         "Skipped  : {0}".format(fso.skipped),
                         "Removed  : {0}".format(fso.removed),
                         "=" * k, "\n"]))

    @staticmethod
    def input(prompt, default=""):
        """ Get input from the user with the specified prompt. """
        # TODO: Handle python 3 input vs. python 2 raw_input
        ret = input(prompt)
        return ret if ret else default


if __name__ == "__main__":
    # Initialize
    settings = Settings.load()
    def_source = settings.get('source', './')
    def_dest = settings.get('dest', './')

    # Start interaction
    UI.show_splash()
    source = UI.input("Source path ({0}) : ".format(def_source), def_source)
    dest = UI.input("Destination path ({0}) : ".format(def_dest), def_dest)
    if not exists(source) or not exists(dest) or source == dest:
        UI.show_message("Invalid paths specified. Aborting...")
        exit(-1)
    else:
        settings['source'], settings['dest'] = source, dest
        Settings.save(settings)

    # Start synchronisation
    sync = SyncHandler()
    sync.clean = False
    sync.sync_folder(abspath(source), dest)

    # Shown summary and close
    UI.show_summary(settings, sync.fso)
