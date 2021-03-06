"""
ZenSync
=======

This module provides simple backup/sync functionality
"""
from os import makedirs, listdir, remove
from os.path import isdir, join, abspath, exists, getsize, sep
from shutil import copy, rmtree
from json import load, dump
import logging


def print_inline(func):
    """ Redraw the entire screen if needed so the output file output lines
    appear in the same place.
    """
    def wrapper(fso, *args):
        # logging.info("{0}: {1} ({2}))".format(
        #     func.__name__.title(), args[-1], args[-2]))
        logging.info("{0}: {1}{2}{3}".format(
            func.__name__.title(), args[-2], sep, args[-1]))
        return func(fso, *args)
    return wrapper


class FileSystemOps(object):
    """
    Handle and log all file operation
    """
    copied, replaced, removed, skipped = 0, 0, 0, 0

    def __init__(self, ui):
        """ Set the UI to display messages """
        self.ui = ui

    def copy(self, source, dest_folder, dest_file):
        """ Copy the source file to the destination. Overwrite if it exists. """

        @print_inline
        def copying(_self, _s, _d, _df):
            """ Dummy function for making use of single decorator for logging"""
            pass

        @print_inline
        def replacing(_self, _s, _d, _df):
            """ Dummy function for making use of single decorator for logging"""
            pass

        dest = join(dest_folder, dest_file)
        if exists(dest):
            replacing(self, source, dest_folder, dest_file)
            self.replaced += 1
        else:
            copying(self, source, dest_folder, dest_file)
            self.copied += 1
        copy(source, dest)

    @print_inline
    def remove(self, dest_folder, dest_file):
        """ Remove the specified file. """
        dest = join(dest_folder, dest_file)
        self.removed += 1
        remove(dest)

    def skip(self, _dest_folder, _dest_file):
        """ Skip processing on the specified file. """
        self.skipped += 1


class Settings(object):
    """
    Handles the loading and saving of system settings via a json file.
    Keys include:
        source    : defaults to "./"
        dest      : defaults to "./"
    """
    store_file = '.zensync.json'
    """ The file used to store our settings."""

    enabled = False
    """ Determines whether or not to use a settings file to store previous
    choices. This is switched of by default for cleaner folders and write-only
    friendliness. """

    @staticmethod
    def load():
        """
        Return a dictionary containing the users previously selected settings
        or te default settings.
        """
        if exists(Settings.store_file) and Settings.enabled:
            with open(Settings.store_file, 'r') as f:
                return load(f)
        else:
            return {'source': './', 'dest': './'}

    @staticmethod
    def save(settings):
        """
        Save the specified dictionary of settings to the store file
        """
        if Settings.enabled:
            with open(Settings.store_file, 'w') as f:
                dump(settings, f)


class SyncHandler(object):
    """
    Handles the synchronization task between two given folders.
    """
    replace = False
    """ Always replace files in the destination. """

    clean = True
    """ Remove files and folders that are not in the source folder """

    def __init__(self, settings, ui):
        self.fso = FileSystemOps(ui)
        self.clean = bool(settings['clean'].lower() == "y")
        self.force = bool(settings['force'].lower() == "y")

    @staticmethod
    def file_different(source, dest):
        """
        Return True if the files are different. The default check is for size
        only.
        """
        return getsize(source) != getsize(dest) or source.endswith(".EPIM")


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
            elif not exists(f_dest) or self.force or \
                    self.file_different(f_source, f_dest):
                if not exists(dest):
                    makedirs(dest)
                self.fso.copy(f_source, dest, item)
            else:
                self.fso.skip(dest, item)

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
            if exists(sub_item) and item not in files:
                if isdir(sub_item):
                    rmtree(sub_item)
                else:
                    self.fso.remove(dest, item)


class UI(object):
    """
    Handles the presentation
    """
    cols = 80

    def __init__(self, settings):
        self.settings = settings

    @staticmethod
    def show_splash():
        print("\n".join(["",
                         "=" * UI.cols,
                         "{:^80}".format("ZenSync"),
                         "=" * UI.cols, "\n"]))

    @staticmethod
    def show_message(msg):
        print(msg)

    @staticmethod
    def show_summary(fso):
        print("\n".join([chr(13),
                         "Copied   : {0}".format(fso.copied),
                         "Replaced : {0}".format(fso.replaced),
                         "Skipped  : {0}".format(fso.skipped),
                         "Removed  : {0}".format(fso.removed),
                         "Log file  : zensync.log",
                         "=" * UI.cols, "\n"]))

    @staticmethod
    def input(prompt, default=""):
        """ Get input from the user with the specified prompt. """
        # TODO: Handle python 3 input vs. python 2 raw_input
        ret = input(prompt)
        return ret if ret else default


if __name__ == "__main__":
    # Initialize
    settings = Settings.load()
    def_source = settings['source']
    def_dest = settings['dest']

    # Start interaction
    ui = UI(settings)
    ui.show_splash()
    settings['source'] = ui.input("Source path ({}): ".format(def_source),
                                  def_source)
    settings['dest'] = ui.input("Destination path ({0}): ".format(def_dest),
                                def_dest)
    settings['clean'] = ui.input(
        "Remove missing? ({}): ".format(settings.get('clean', 'n')), 'n')
    settings['force'] = ui.input(
        "Force overwrite? ({}): ".format(settings.get('force', 'n')), 'n')

    source, dest = settings['source'], settings['dest']
    if not exists(source) or not exists(dest) or source == dest:
        ui.show_message("Invalid paths specified. Aborting...")
    else:
        Settings.save(settings)

    # Start synchronisation

    # # Complete loging
    # logging.basicConfig(filename="zensync.log",
    #                     filemode="w",
    #                     format='%(asctime)-15s : %(message)s',
    #                     level=logging.INFO)

    # # Display only the message
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    logging.info(" = ZenSync = \n\nSettings: " + str(settings) + "\n")
    sync = SyncHandler(settings, ui)
    sync.sync_folder(abspath(source), abspath(dest))

    # Shown summary and close
    ui.show_summary(sync.fso)
