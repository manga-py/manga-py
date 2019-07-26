import atexit
from shutil import rmtree
from sys import stderr

from manga_py.exceptions import ProviderNotFoundException
from manga_py.libs import print_lib
from manga_py.libs.info.glob import InfoGlobal
from manga_py.libs.log import logger
from manga_py.libs.provider import Provider
from manga_py.manga import Manga
from manga_py.providers import get_provider
from . import args
from ._helper import CliHelper
from .args.args_helper import ArgsListHelper
from .db import DataBase


class Cli(CliHelper):
    __slots__ = ('log',)
    db = DataBase()
    info = InfoGlobal()

    def __init__(self):
        super().__init__()
        atexit.register(self.exit)
        self.log = logger(self.args.log_to_file)

    def exit(self):
        # remove temp directory
        if not self.args.do_not_clear_temporary_directory:
            rmtree(self.temp_path)
            print('Temporary directory: \n %s' % self.temp_path)

    def run(self):
        urls = self.args.url

        if self.args.force_clean:
            # TODO
            pass

        # if self.args.get('title'):  # todo: Maybe search for user-urls only
        #     urls = self.search_for_title(self.args.title)

        self.print(
            'temp_path: ' + self.temp_path,
        )
        self.log.info('temp_path: ' + self.temp_path)

        self.args.force_make_db and self.db.clean()

        if self.args.update_all:
            self.print('Soon')
            exit(1)
            self._update_all()
        elif len(urls) < 1:
            self.log.warning('Urls list has empty')
            self.raw_args.print_help()
            exit(1)
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
                print_lib(e.args, file=stderr)
