"""
ZenSync
=======

This module provides simple backup/sync functionality
"""
from os import makedirs, listdir, remove, system
from os.path import isdir, join, abspath, exists, getsize
from shutil import copy
from json import load, dump


def reset_render(func):
    """ Redraw the entire screen if needed so the output file output lines
    appear in the same place.
    """
    def wrapper(fso, *args):

        fso.ui.render()
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
        dest = join(dest_folder, dest_file)
        if exists(dest):
            self.ui.show_message("Replacing: ", dest)
            self.replaced = self.replaced + 1
        else:
            self.ui.show_message("Copying: ", dest)
            self.copied = self.copied + 1  # Do not use += 1!
        copy(source, dest)

    def remove(self, dest_folder, dest_file):
        """ Remove the specified file. """
        dest = join(dest_folder, dest_file)
        self.ui.show_message("Removing: ", dest)
        self.removed = self.removed + 1
        remove(dest)

    @reset_render
    def skip(self, dest_folder, dest_file):
        """ Skip processing on the specified file. """
        dest = join(dest_folder, dest_file)
        self.ui.show_message("Skipping: ", dest)
        self.skipped = self.skipped


class Settings(object):
    """
    Handles the loading and saving of system settings via a json file.
    Keys include:
        source    : defaults to "./"
        dest      : defaults to "./"
        clean     : defaults tp False
        log_level : defaults to 2
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
            return {'source': './', 'dest': './'}

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

    def __init__(self, settings, ui):
        self.fso = FileSystemOps(ui)
        self.clean = settings.get('clear', False)

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
            if not isdir(sub_item) and item not in files:
                self.fso.remove(dest, item)


class UI(object):
    """
    Handles the presentation
    """
    cols = 80

    def __init__(self, settings):
        self.settings = settings

    def render(self, fso=None):
        """ Generate the screen and UI element displaying the current settings
        and fso state (if not None).
        """
        system("clear")
        self.show_splash()
        ui.show_settings()

    def show_splash(self):
        print("\n".join(["=" * UI.cols,
                         "{:^80}".format("ZenSync"),
                         "=" * UI.cols, "\n"]))

    def show_settings(self):
        """ Display the currently active settings. """
        print("\n".join([
               "Source    : {0}".format(settings['source']),
               "Dest      : {0}".format(settings['dest']),
               "Clean     : {0}".format(
                   "Y" if settings.get("clean", True) else "N"),
               "Log level : {0}".format(settings.get("log_level", 2)),
               "=" * self.cols]))

    @staticmethod
    def show_message(msg, folder='', file=''):
        """ Display a message. If a folder and file are specified, the out is
        truncated to fit into the 80 column screen.
        """

        if folder:
            out = "{0:<15} {1:<50} {2:<15} "
            print(out.format(msg, folder[-49:], file))
        else:
            print(msg)

    @staticmethod
    def show_summary(fso):
        print("\n".join([chr(13),
                         "Copied   : {0}".format(fso.copied),
                         "Replaced : {0}".format(fso.replaced),
                         "Skipped  : {0}".format(fso.skipped),
                         "Removed  : {0}".format(fso.removed),
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
    inp, step, ui = "", 0, UI(settings)
    while True:
        ui.render()
        if step == 0:
            inp = ui.input("Source path : ", def_source)
            settings['source'] = inp
        elif step == 1:
            inp = ui.input("Destination path : ", def_dest)
            settings['dest'] = inp
        else:
            source, dest = settings['source'], settings['dest']
            if not exists(source) or not exists(dest) or source == dest:
                ui.show_message("Invalid paths specified. Aborting...")
                exit(-1)
            else:
                Settings.save(settings)

            # Start synchronisation
            sync = SyncHandler(settings, ui)
            sync.sync_folder(abspath(source), dest)

            # Shown summary and close
            ui.show_summary(sync.fso)
            inp = "q"

        if inp.lower() == "q":
            break
        else:
            step += 1
