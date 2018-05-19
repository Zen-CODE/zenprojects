"""
ZenSync
=======

This module provides simple backup/sync functionality
"""
from os import makedirs, walk
from os.path import isdir, join, abspath, exists, getsize
from shutil import copy


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

    # TODO: Implement
    follow_symlinks = False

    def file_different(self, source, dest):
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
        for dirname, subdirs, files in walk(source):
            for fname in files:
                full_name = join(dirname, fname)
                full_dest = join(dest, fname)
                if not exists(full_dest):
                    UI.show_message("Copying to {0}".format(full_dest))
                    makedirs(dest)
                    copy(full_name, full_dest,
                         follow_symlinks=self.follow_symlinks)
                elif self.file_different(full_name, full_dest):
                    UI.show_message(
                        "Replacing file: {0}".format(full_dest))
                    copy(full_name, full_dest,
                         follow_symlinks=self.follow_symlinks)
                else:
                    UI.show_message(
                        "File unchanged, skipping: {0}".format(full_dest))
            [self.sync_folder(join(dirname, f_dir), join(dest, f_dir))
             for f_dir in subdirs]

    def clean_dest(self, source, dest):
        """
        Remove files that are in the dest folder and not in the source:
        """


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
    sync.sync_folder(abspath(path), dest)
