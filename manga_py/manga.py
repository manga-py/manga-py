from pathlib import Path
from typing import Optional, List, Callable

from progressbar import ProgressBar

from .cli.args.args_helper import ArgsListHelper
from .libs import db
from .libs import print_lib
from .libs.fs import check_free_space, temp_path, user_path
from .libs.http import default_ua
from .libs.provider import Provider
from .libs.store import Store
from .exceptions import SpaceLeftException
from .libs.log import logger


class Manga:
    __slots__ = ('provider', 'arguments', 'db', 'store', 'progressbar', '_', 'file_callbacks', 'logger')

    def __init__(self):
        self.store = Store()
        self.provider = None  # type: Optional[Provider]
        self.arguments = self.store.arguments  # type: ArgsListHelper
        self.db = None  # type: Optional[db.Manga]
        self.progressbar = None  # type: Optional[ProgressBar]
        self._ = None  # type: Optional[dict]
        self.file_callbacks = []  # type: List[Callable]
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
        self._ = {}  # temporary provider store
        self.logger.info('Provider: %s' % provider.__class__.__name__)

        # if self.arguments.allow_progress:
        #     self.progressbar = ProgressBar()

        self.provider = provider
        self.provider.prepare()
        self.store.content = self.provider.get_main_content()

        self.run_pages()

    def run_pages(self):
        pass

    def add_file_callback(self, callback: Callable):
        self.file_callbacks.append(callback)


__all__ = ['Manga']
