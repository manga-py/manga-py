from .chapter import Chapter
from .file import File
from typing import overload


class Callbacks:
    def before_chapter(self, chapter: Chapter):
        pass

    def after_chapter(self, chapter: Chapter):
        pass

    @overload
    def before_download(self, file: File):
        pass

    def before_download(self, chapter: Chapter):
        pass

    @overload
    def after_download(self, file: File):
        pass

    def after_download(self, chapter: Chapter):
        pass
