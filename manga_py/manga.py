from pathlib import Path
from typing import Optional, List, Callable

from progressbar import ProgressBar

from .cli.args.args_helper import ArgsListHelper
from .libs import db
from .libs.fs import check_free_space, temp_path, user_path
from .libs.http import default_ua
from .libs.provider import Provider
from .libs.store import store
from .exceptions import SpaceLeftException, JsonException
from .libs.log import logger
from .libs.provider.file_tuple import *


class Manga:
    __slots__ = ('provider', 'arguments', 'db', 'store', 'progressbar', '_tmp', 'file_callbacks', 'logger', 'print')

    def __init__(self, _print: Callable[..., None] = None):
        if _print is None:
            from .cli import syslog
            self.print = syslog

        self.store = store
        self.provider = None  # type: Optional[Provider]
        self.arguments = self.store.arguments  # type: ArgsListHelper
        self.db = None  # type: Optional[db.Manga]
        self.progressbar = None  # type: Optional[ProgressBar]
        self._tmp = None  # type: Optional[dict]
        self.file_callbacks = []  # type: List[Callable]
        self.print = _print
        if not self.arguments.do_not_use_database:
            db.make_db(self.arguments.force_make_db)
            self.db = db.Manga()
        if self.store.ua is None and not self.arguments.update_all:
            self.store.ua = default_ua()

        self.logger = logger()
        if not check_free_space(Path(self.arguments.destination), self.arguments.min_free_space):
            # check free space for destination directory
            self.logger.critical('No space left on %s' % self.arguments.destination)
            raise SpaceLeftException(self.arguments.destination)
        temp = temp_path()
        if not check_free_space(temp, 150):
            # check free space for temporary directory (minimum 150Mb)
            self.logger.critical('No space left on %s' % temp)
            raise SpaceLeftException(temp)
        _user_path = user_path()
        if not check_free_space(_user_path, 150):
            # check free space for system directory (minimum 150Mb)
            self.logger.critical('No space left on %s' % _user_path)
            raise SpaceLeftException(_user_path)

    def run(self, provider: Provider):
        self._tmp = {}  # temporary provider store

        provider_class = 'Provider: %s' % provider.__class__.__name__
        if self.arguments.debug:
            self.print(provider_class)

        # if self.arguments.allow_progress:
        #     self.progressbar = ProgressBar()

        self.provider = provider

        self.provider.set_print(self.print)  # init print function
        self.provider.prepare()
        try:
            self.store.content = self.provider.get_main_content()
        except JsonException as e:
            self.logger.warning(('Error!', e.args, e.content()))
            return

        self.run_pages()

    def run_pages(self):
        for chapter in self.provider.chapters():  # type: ChapterTuple
            files = self.provider.chapter_files(chapter)
            self.run_download_files(chapter.idx, files)

    def run_download_files(self, idx: str, files: ChapterFilesTuple):
        self._tmp['chapter_files'] = []
        if files.archive is not None:
            path = Path(self.arguments.destination or 'Manga')
            path.mkdir(exist_ok=True)
            file = self.provider.download(idx, files.archive, path.joinpath('chapter-{:0>3}'.format(idx)), TYPE_ARCHIVE)
            self._tmp['chapter_files'].append(file)
        for file_idx, url in enumerate(files.images or []):
            path = self.provider.temp_path().joinpath('image-{:0>3}-{:0>3}{}'.format(idx, file_idx, Path(url).suffix))
            file = self.provider.download(str(file_idx), url, path, TYPE_IMAGE)
            self._tmp['chapter_files'].append(file)

    def add_file_callback(self, callback: Callable):
        self.file_callbacks.append(callback)


__all__ = ['Manga']
