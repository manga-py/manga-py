from abc import ABCMeta

from .libs.base import Base
from .libs.db import Manga
from .libs.base.verify import Verify
from .libs.base.chapter import Chapter
from .libs.base.file import File


class Provider(Base, metaclass=ABCMeta):
    _db = None
    _store = None

    def __init__(self):
        super().__init__()
        self._store = {}
        self._db = Manga()

    def run(self, args: dict):
        Verify(args).check()
        super()._args = args

    def loop_chapters(self):
        for idx, chapter in enumerate(self.chapters):
            self.chapter = Chapter(idx, chapter, self)
            self.loop_files()

    def loop_files(self):
        for idx, data in enumerate(self.files):
            try:
                file = File(idx, data, self)
                self.download(file)
            except AttributeError:
                pass

    def update_db(self):
        """
        Called twice.
        After receiving the content of the main page and after the completion of work.
        Updates the current manga data in the database.
        :return:
        """
        db = self._db.select().where(Manga.url == self.domain)
        pass
