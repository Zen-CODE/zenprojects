"""
ZenSync
=======

This module provides simple backup/sync functionality
"""
from os import makedirs, walk, listdir
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

    def _process_files(self, dirname, files, dest):
        """
        Process the litt of files
        """
        for fname in files:
            full_name = join(dirname, fname)
            full_dest = join(dest, fname)
            if not exists(full_dest):
                UI.show_message("Copying to {0}".format(full_dest))
                if not exists(dest):
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

    def sync_folder(self, source, dest):
        """
        Synchronizes the contents of the sources and destination folder.
        """
        for dirname, subdirs, files in walk(source):
            self._process_files(dirname, files, dest)
            # Process folders
            [self.sync_folder(join(dirname, f_dir), join(dest, f_dir))
             for f_dir in subdirs]

            if self.clean:
                self._clean_dest(dirname, files, dest)

    def _clean_dest(self,  dirname, files, dest):
        """
        Remove files that are in the dest folder and not in the source.

            files: the list of files in dirname
        """
        if not exists(dest):
            return
        for item in listdir(dest):
            sub_item = join(dest, item)
            if not isdir(sub_item) and item not in files:
                UI.show_message(("Removing {0}".format(sub_item)))
                # TODO: Implement

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
