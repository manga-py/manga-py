from logging import warning, error
from os import path
from zipfile import ZipFile, ZIP_DEFLATED

from manga_py.fs import is_file, make_dirs, basename, dirname, unlink, get_temp_path
from manga_py.manga_image import MangaImage


class Archive:
    _archive = None
    _writes = None
    files = None
    not_change_files_extension = False
    no_webp = False
    error_list = []

    @property
    def has_error(self):
        return self.error_list != []

    def __init__(self):
        self.files = []
        self._writes = {}

    def write_file(self, in_arc_name, data):
        self._writes[in_arc_name] = data

    def add_file(self, file, in_arc_name=None):
        if in_arc_name is None:
            in_arc_name = basename(file)
        if self.__test_is_image(file):
            self.files.append((file, in_arc_name))

    def __add_files(self):
        for file in self.files:
            if is_file(file[0]):
                file = self._file(file)
                self._archive.write(*file)
            else:
                warning('"%s" it\'s not file! Skip' % file[0])

    def _file(self, file):
        ext = self.__update_image_extension(file[0])
        if self.no_webp and ext[ext.rfind('.'):] == '.webp':
            jpeg = ext[:ext.rfind('.')] + '.jpeg'
            jpeg_path = path.join(dirname(file[0]), jpeg)
            MangaImage(file[0]).convert(jpeg_path)
            file = jpeg_path, jpeg
        elif ext:
            file = file[0], ext
        return file

    def __test_is_image(self, _path):
        if not MangaImage.is_image(_path):
            self.error_list.append('File "%s" isn\'t image' % _path)
            warning('File "%s" isn\'t image' % _path)
            return False
        return True

    def __add_writes(self):
        for file in self._writes:
            self._archive.writestr(file, self._writes[file])

    def make(self, dst: str):
        if not len(self.files):
            error('Files list empty. Skip making archive')
            return

        if self.has_error:
            warning('Archive %s have missed files' % dst)
            self.error_list = []

        make_dirs(dirname(dst))

        self._archive = ZipFile(dst, 'w', ZIP_DEFLATED)
        try:
            self.__add_files()
            self.__add_writes()
            self._archive.close()
        except OSError as e:
            self._archive.close()
            raise e
        self._maked()

    def _maked(self):
        for file in self.files:
            try:
                unlink(file[0])
            except Exception:
                error('File %s can\'t deleted' % file[0])

    def __update_image_extension(self, filename) -> str:
        fn, extension = path.splitext(filename)
        if not self.not_change_files_extension:
            ext = MangaImage.real_extension(get_temp_path(filename))
            if ext:
                extension = ext
        return basename(fn + extension)
