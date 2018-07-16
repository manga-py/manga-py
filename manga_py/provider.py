from abc import ABCMeta

from .libs.base import Base
from .libs.base.chapter import Chapter
from .libs.base.file import File
from .libs.db import Manga
from .libs.fs import get_temp_path
from .libs.http.multi_threads import MultiThreads
from .libs.modules.verify import Verify
from .libs.modules.api import Api


class Provider(Base, metaclass=ABCMeta):
    _db = None
    _store = None
    _threads = None
    _progress = None
    _api = None
    temp_path_location = None
    chapter_idx = None

    def __init__(self):
        super().__init__()
        self.temp_path_location = get_temp_path()
        self._store = {}
        self._db = Manga()
        self._threads = MultiThreads()
        if not self.arg('no-progress') and self.progressbar:
            self._progress = self.progressbar()
        if self.arg('no_multi_threads'):
            self._threads.max_threads = 1
        Api(self)

    def run(self, args: dict):
        Verify(args).check()
        super()._args = args

    def loop_chapters(self):
        for idx, data in enumerate(self.chapters):
            self.chapter_idx = idx
            if isinstance(data, dict):
                pass
            else:
                self.chapter = Chapter(idx, data, self)
                self.loop_files()

    def loop_files(self):
        self.progress_next()
        for idx, data in enumerate(self.files):
            try:
                file = File(idx, data, self)
                self.download(file)
            except AttributeError:
                pass
        self._threads.start(self.progress_next)

    def download(self, file: File):
        self._threads.add(target=super().download, args=(file,))

    def progress_next(self, new=False):
        """
        :param new:
        :return:
        """
        if self._progress:
            if new:
                self._progress.value > 0 and self._progress.finish()
                self._progress.start(len(self._threads.threads))
            else:
                self._progress.update(self._progress.value + 1)

    def update_db(self):
        """
        Called twice.
        After receiving the content of the main page and after the completion of work.
        Updates the current manga data in the database.
        :return:
        """
        db = self._db.select().where(Manga.url == self.domain)
