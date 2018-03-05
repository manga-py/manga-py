from zipfile import ZipFile, ZIP_DEFLATED

from src.fs import is_file, make_dirs, basename, dirname, unlink
from os.path import splitext


class Archive:
    files = None

    def __init__(self):
        self.files = []

    @staticmethod
    def _check_ext(name):
        name, ext = splitext(name)
        if ext == '' or ext == '.':
            return name + '.png'
        return name

    def add_file(self, file, in_arc_name=None):
        if in_arc_name is None:
            in_arc_name = self._check_ext(basename(file))
        self.files.append((file, in_arc_name))

    def set_files_list(self, files):
        self.files = files

    def make(self, dist, info_file=None):
        if not len(self.files):
            return

        make_dirs(dirname(dist))
        archive = ZipFile(dist, 'w', ZIP_DEFLATED)

        for file in self.files:
            if is_file(file[0]):
                archive.write(file[0], file[1])
            else:
                print(file[0], ' - IS NOT FILE!!!')

        info_file and archive.writestr('info.txt', info_file)

        archive.close()

        self._maked()

    def _maked(self):
        for file in self.files:
            unlink(file[0])
