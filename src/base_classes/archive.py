from zipfile import ZipFile, ZIP_DEFLATED

from src.fs import is_file, make_dirs, basename, dirname, unlink


class Archive:
    files = None

    def __init__(self):
        self.files = []

    def add_file(self, file, in_arc_name=None):
        if in_arc_name is None:
            in_arc_name = basename(file)
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
