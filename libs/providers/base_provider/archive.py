from zipfile import ZipFile, ZIP_DEFLATED

from libs.fs import is_file, make_dirs, basename, dirname, unlink


class Archive:

    def __init__(self):
        self.files = []

    def add_file(self, file):
        self.files.append(file)

    def set_files_list(self, files):
        self.files = files

    def make(self, dist, info_file=None):
        if not len(self.files):
            print('files == [] archive.py:19')
            return

        make_dirs(dirname(dist))
        archive = ZipFile(dist, 'w', ZIP_DEFLATED)

        for file in self.files:
            if is_file(file):
                archive.write(file, basename(file))

        info_file and archive.writestr('info.txt', info_file)

        archive.close()

        self._maked()

    def _maked(self):
        for file in self.files:
            unlink(file)
