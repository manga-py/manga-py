from typing import Optional

from progressbar import ProgressBar

from manga_py.cli.args import ArgsListHelper
from manga_py.libs import db
from manga_py.libs import print_lib
from manga_py.libs.http import default_ua
from manga_py.libs.provider import Provider
from manga_py.libs.store import Store
from manga_py.libs.fs import check_free_space
from pathlib import Path


class Manga:
    __slots__ = ('provider', 'arguments', 'db', 'store', 'progressbar')

    def __init__(self):
        self.store = Store()
        self.provider = None  # type: Optional[Provider]
        self.arguments = self.store.arguments  # type: ArgsListHelper
        self.db = None  # type: Optional[db.Manga]
        self.progressbar = None  # type: Optional[ProgressBar]
        if not self.arguments.do_not_use_database:
            db.make_db(self.arguments.force_make_db)
            self.db = db.Manga()
        if self.store.ua is None and not self.arguments.update_all:
            self.store.ua = default_ua()
        if not check_free_space(Path(self.arguments.destination), self.arguments.min_free_space):
            raise RuntimeError('No space left on device')

    def run(self, provider: Provider):
        if self.arguments.verbose_log:
            print_lib('Provider: %s' % provider.__class__.__name__)

        # if self.arguments.allow_progress:
        #     self.progressbar = ProgressBar()

        self.provider = provider
        self.provider.prepare()
        self.store.content = self.provider.get_main_content()

        self.run_pages()

    def run_pages(self):
        pass


__all__ = ['Manga']
