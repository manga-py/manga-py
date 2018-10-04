from .chapter import Chapter
from .file import File
from typing import Union


class Callbacks:
    def before_chapter(self, chapter: Chapter):
        pass

    def after_chapter(self, chapter: Chapter):
        pass

    def before_download(self, item: Union[File, Chapter]):
        pass

    def after_download(self, file: Union[File, Chapter]):
        pass
