import atexit
from shutil import rmtree
from logging import DEBUG

from manga_py.exceptions import ProviderNotFoundException
from manga_py.libs.info.glob import InfoGlobal
from manga_py.libs.log import logger
# from manga_py.libs.provider import Provider
from manga_py.manga import Manga
from manga_py.providers import get_provider
from . import args
from ._helper import *
from .db import DataBase


class Cli(_helper.CliHelper):
    __slots__ = ('log',)
    db = DataBase()
    info = InfoGlobal()

    def __init__(self):
        super().__init__()
        atexit.register(self.exit)
        self.log = logger(self.args.log_to_file)
        if self.args.debug:
            self.log.setLevel(DEBUG)

    def exit(self):
        # remove temp directory
        if self.args.clear_temporary_directory:
            rmtree(self.temp_path)
        else:
            syslog('Temporary directory: \n {}'.format(self.temp_path))

    def run(self):
        urls = self.args.url

        if self.args.force_clean:
            # TODO
            pass

        # if self.args.get('title'):  # todo: Maybe search for user-urls only
        #     urls = self.search_for_title(self.args.title)

        if self.args.debug:
            syslog(
                'temp_path: {}'.format(self.temp_path),
            )

        self.log.info('temp_path: {}'.format(self.temp_path))

        self.args.force_make_db and self.db.clean()

        if self.args.update_all:
            syslog('Soon')
            exit(1)
            self._update_all()
        elif len(urls) < 1:
            self.log.warning('Urls list has empty')
            self._print_cli_help()
            exit(1)
        else:
            self._run_normal(urls)

    def _update_all(self):
        raise RuntimeError('Soon')

    def _run_normal(self, urls):
        for url in urls:
            try:
                for provider in get_provider(url, self.args):
                    manga = Manga(_print=syslog)
                    manga.run(provider)
            except ProviderNotFoundException as e:
                syserr(e.args[0])


__all__ = ['Cli', 'syslog', 'syserr']
