from zipfile import ZipFile, ZIP_DEFLATED

# from PIL import Image as PilImage
from manga_py.image import Image
from os import path
from time import sleep

from manga_py.fs import is_file, make_dirs, basename, dirname, unlink, get_temp_path


class Archive:
    _archive = None
    _writes = None
    files = None
    not_change_files_extension = False
    no_webp = False
    has_error = False

    def __init__(self):
        self.files = []
        self._writes = {}

    def write_file(self, data, in_arc_name):
        self._writes[in_arc_name] = data

    def add_file(self, file, in_arc_name=None):
        if in_arc_name is None:
            in_arc_name = basename(file)
        self.files.append((file, in_arc_name))

    def set_files_list(self, files):
        self.files = files

    def add_book_info(self, data):
        self.write_file('comicbook.xml', data)

    def __add_files(self):
        for file in self.files:
            if is_file(file[0]):
                ext = self.__update_image_extension(file[0])
                if self.no_webp and ext[ext.rfind('.'):] == '.webp':
                    jpeg = ext[:ext.rfind('.')] + '.jpeg'
                    jpeg_path = path.join(dirname(file[0]), jpeg)
                    Image(file[0]).convert(jpeg_path)
                    file = jpeg_path, jpeg
                elif ext:
                    file = file[0], ext
                self._archive.write(*file)

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
        try:
            self.__add_files()
            self.__add_writes()
            self._archive.close()
        except OSError as e:
            self._archive.close()
            raise e
        self._archive.close()
        self._maked()

    def _maked(self):
        for file in self.files:
            unlink(file[0])

    def __update_image_extension(self, filename) -> str:
        fn, extension = path.splitext(filename)
        if not self.not_change_files_extension:
            ext = Image.real_extension(get_temp_path(filename))
            if ext:
                extension = ext
        return basename(fn + extension)
