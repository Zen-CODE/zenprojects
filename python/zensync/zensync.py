"""
ZenSync
=======

This module provides simple backup/sync functionality
"""
from os import makedirs, walk, listdir, remove
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
    clean = True
    """ Remove files that are not in the source folder """

    # TODO: Implement
    follow_symlinks = False

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
            elif not exists(f_dest):
                if not exists(dest):
                    makedirs(dest)
                UI.show_message("Copying to {0}".format(f_dest))
                copy(f_source, f_dest, follow_symlinks=self.follow_symlinks)
            elif self.file_different(f_source, f_dest):
                UI.show_message("Replacing file {0}".format(f_dest))
                copy(f_source, f_dest, follow_symlinks=self.follow_symlinks)
            else:
                UI.show_message("Skipping file {0}".format(f_dest))

        if self.clean:
            self._clean_dest(files, dest)


    @staticmethod
    def _clean_dest(files, dest):
        """
        Remove files that are in the dest folder and not in the source.

            files: the list of files in that should NOT be removed
        """
        if not exists(dest):
            return
        for item in listdir(dest):
            sub_item = join(dest, item)
            if not isdir(sub_item) and item not in files:
                UI.show_message(("Removing {0}".format(sub_item)))
                remove(sub_item)


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
