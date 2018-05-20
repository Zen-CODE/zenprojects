"""
ZenSync
=======

This module provides simple backup/sync functionality
"""
from os import makedirs, listdir, remove
from os.path import isdir, join, abspath, exists, getsize
from shutil import copy


class FileSystemOps(object):
    """
    Handle and log all file operation
    """
    follow_symlinks = False

    copied, replaced, removed, skipped = 0, 0, 0, 0

    def copy(self, source, dest):
        """ Copy the source file to the destination. Overwrite if it exists. """
        if exists(dest):
            UI.show_message("Copying to {0}".format(dest))
            self.copied = self.copied + 1  # Do not use += 1!
        else:
            UI.show_message("Replacing file {0}".format(dest))
            self.replaced = self.replaced + 1
        copy(source, dest, follow_symlinks=self.follow_symlinks)

    def remove(self, dest):
        """ Remove the specified file. """
        UI.show_message(("Removing {0}".format(dest)))
        self.removed = self.removed + 1
        remove(dest)

    def skip(self, dest):
        """ Skip processing on the specified file. """
        UI.show_message("Skipping file {0}".format(dest))
        self.skipped = self.skipped


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
    @staticmethod
    def show_splash():
        print("\n".join(["=" * 11, "= ZenSync =", "=" * 11, "\n"]))

    @staticmethod
    def show_message(msg):
        """ Display a message during processing. """
        print(msg)


if __name__ == "__main__":
    path = "/home/richard/Temp/zensync_source"
    dest = "/home/richard/Temp/zensync_dest"

    UI.show_splash()
    sync = SyncHandler()
    sync.clean = True
    sync.sync_folder(abspath(path), dest)
