import atexit
from shutil import rmtree

from manga_py.cli import args
from manga_py.cli._helper import CliHelper
from manga_py.cli.args import ArgsListHelper
from manga_py.cli.db import DataBase
from manga_py.exceptions import ProviderNotFoundException
from manga_py.libs.info.glob import InfoGlobal
from manga_py.libs.log import logger
from manga_py.libs.provider import Provider
from manga_py.libs.store import Store
from manga_py.manga import Manga
from manga_py.providers import get_provider


class Cli(CliHelper):
    __slots__ = ()
    db = DataBase()
    info = InfoGlobal()
    log = logger()

    def __init__(self):
        super().__init__()
        atexit.register(self.exit)
        Store().arguments = self.args

    def exit(self):
        # remove temp directory
        if self.args.do_not_clear_temporary_directory:
            rmtree(self.temp_path)
            print('Temporary directory: \n' + self.temp_path)

    def run(self):
        urls = self.args.url

        # if self.args.get('title'):  # todo: Maybe search for user-urls only
        #     urls = self.search_for_title(self.args.title)

        if self.show_log():
            self.print(
                'temp_path: ' + self.temp_path,
            )

        self.args.force_make_db and self.db.clean()

        if self.args.update_all:
            self.print('Soon')
            exit(1)
            self._update_all()
        else:
            self._run_normal(urls)

    def _update_all(self):
        raise RuntimeError('Soon')

    def _run_normal(self, urls):
        for url in urls:
            try:
                provider = get_provider(url, self.args)  # type: Provider
                manga = Manga()
                manga.run(provider)
            except ProviderNotFoundException as e:
                self.print(e.args)
