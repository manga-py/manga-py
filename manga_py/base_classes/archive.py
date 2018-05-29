from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image

from manga_py.fs import is_file, make_dirs, basename, dirname, unlink
from os.path import splitext


class Archive:
    _archive = None
    files = None
    _writes = None

    def __init__(self):
        self.files = []
        self._writes = {}

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

    def write_file(self, data, in_arc_name):
        self._writes[in_arc_name] = data

    def add_file(self, file, in_arc_name=None):
        if in_arc_name is None:
            in_arc_name = basename(file)
        in_arc_name = self._check_ext(file, in_arc_name)
        self.files.append((file, in_arc_name))

    def set_files_list(self, files):
        self.files = files

    def add_book_info(self, data):
        self.write_file('comicbook.xml', data)

    def __add_files(self):
        for file in self.files:
            if is_file(file[0]):
                self._archive.write(file[0], file[1])

    def __add_writes(self):
        for file in self._writes:
            self._archive.writestr(file, self._writes[file])

    def add_info(self, data):
        self.write_file(data, 'info.txt')

    def make(self, dst):
        if not len(self.files) and not len(self._writes):
            return

        make_dirs(dirname(dst))

        self._archive = ZipFile(dst, 'w', ZIP_DEFLATED)
        self.__add_files()
        self.__add_writes()
        self._archive.close()
        self._maked()

    def _maked(self):
        for file in self.files:
            unlink(file[0])
