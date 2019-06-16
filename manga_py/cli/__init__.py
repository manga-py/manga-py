import atexit
import json
from shutil import rmtree
from typing import Union, Dict

from manga_py.libs.log import logger

from manga_py.libs.info.glob import InfoGlobal
from manga_py.libs.info import Info
from manga_py.cli.args import ArgsListHelper
from . import args
from ._helper import CliHelper
from .db import DataBase
from manga_py.libs import fs
from manga_py.providers import get_provider


class Cli(CliHelper):
    __slots__ = ()
    db = DataBase()
    info = InfoGlobal()
    log = logger()

    def __init__(self):
        super().__init__()
        atexit.register(self.exit)

    def exit(self):
        # remove temp directory
        if self.args.get('do_not_clear_temporary_directory'):
            rmtree(self.temp_path)
            print('Temporary directory: \n' + self.temp_path)

    def run(self):
        urls = self.args.url

        # if self.args.get('title'):  # todo: Maybe search for user-urls only
        #     urls = self.search_for_title(self.args.get('title'))

        if self.show_log():
            self.print(
                'temp_path: ' + self.temp_path,
            )

        self.args.get('force_make_db', False) and self.db.clean()

        if self.args.get('update_all'):
            self.print('Soon')
            exit(1)
            self._update_all()
        else:
            if len(urls) > 1:
                self.args['name'] = None
                self.args['skip_volumes'] = None
                self.args['max_volumes'] = None
            self._run_normal(urls)

    def _update_all(self):
        default_args = self.get_default_args()
        for manga in self.db.get_all():  # type: Manga
            self.show_log() and self.log.info('Update %s', manga.url)
            _args = default_args.copy()
            data = json.loads(manga.data)
            data_args = data.get('args', {})
            del data_args['rewrite_exists_archives']
            del data_args['user_agent']
            del data_args['url']

            if not fs.is_dir(fs.path_join(data_args['destination'], data_args['name'])):
                self.show_log() and self.log.warning('Destination not exists. Skip')
                continue

            _args.update({  # re-init args
                'url': manga.url,
                **data_args,
            })
            provider = self._get_provider(_args)  # type: Provider
            if provider:
                provider.before_provider(_args)
                provider.http.cookies = data.get('cookies')
                provider.http.ua = data.get('browser')
                provider.run(_args)
                provider.after_provider()
                provider.update_db()
                self.global_info.add_info()  # TODO
            else:
                self.show_log() and self.log.error('Provider not exists')

    def _run_normal(self, urls):
        for url in urls:
            self.args['url'] = url
            provider = get_provider(self.args)  # type: Provider
            if provider:
                provider.before_provider(self.args)
                provider.run(self.args)
                provider.after_provider()
                provider.update_db()
                # self.global_info.add_info(info)
            else:
                self.show_log() and self.log.warning('Provider not exists')
