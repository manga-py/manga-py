from .chapter import Chapter
from .file import File


class Callbacks:
    def before_chapter(self, chapter: Chapter):
        pass

    def after_chapter(self, chapter: Chapter):
        pass

    def before_download(self, file: File):
        pass

    def after_download(self, file: File):
        pass
