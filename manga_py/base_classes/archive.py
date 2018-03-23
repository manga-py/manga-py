from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image

from manga_py.fs import is_file, make_dirs, basename, dirname, unlink
from os.path import splitext


class Archive:
    files = None

    def __init__(self):
        self.files = []

    @staticmethod
    def _check_ext(file, name):
        file_name, file_ext = splitext(name)
        if file_ext == '' or file_ext == '.':
            try:
                image = Image.open(file)
                name = file_name.rstrip('.') + '.' + image.format.lower()
                image.close()
            except (FileNotFoundError, OSError):
                pass
        return name

    def add_file(self, file, in_arc_name=None):
        if in_arc_name is None:
            in_arc_name = basename(file)
        in_arc_name = self._check_ext(file, in_arc_name)
        self.files.append((file, in_arc_name))

    def set_files_list(self, files):
        self.files = files

    def make(self, dst, info_file=None):
        if not len(self.files):
            return

        make_dirs(dirname(dst))
        archive = ZipFile(dst, 'w', ZIP_DEFLATED)

        for file in self.files:
            if is_file(file[0]):
                archive.write(file[0], file[1])

        info_file and archive.writestr('info.txt', info_file)

        archive.close()

        self._maked()

    def _maked(self):
        for file in self.files:
            unlink(file[0])
