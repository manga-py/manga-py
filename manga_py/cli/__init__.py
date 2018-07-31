import atexit
import json
from shutil import rmtree

import better_exceptions
from zenlog import log

from manga_py.libs import fs
from manga_py.libs.modules import info
from . import args
from ._helper import CliHelper
from .db import DataBase


class Cli(CliHelper):
    db = None

    def __init__(self):
        self._temp_path = fs.get_temp_path()
        atexit.register(self.exit)
        fs.make_dirs(self._temp_path)
        self.global_info = info.InfoGlobal()
        self.db = DataBase()

    def exit(self):
        # remove temp directory
        rmtree(self._temp_path)

    def run(self):
        better_exceptions.hook()
        _args = self._args.copy()
        self._print_cli_help()
        urls = _args.get('url', []).copy()
        _args.get('force_make_db', False) and self.db.clean()
        if self._args.get('update_all'):
            self._update_all()
        else:
            if len(urls) > 1:
                _args['name'] = None
                _args['skip_volumes'] = None
                _args['max_volumes'] = None
            self._run_normal(_args, urls)

    def _update_all(self):
        default_args = self.get_default_args()
        for manga in self.db.get_all():  # type Manga
            self.log() and log.info('Update %s', manga.url)
            _args = default_args.copy()
            data = json.loads(manga.data)
            data_args = data.get('args', {})
            del data_args['rewrite_exists_archives']
            del data_args['user_agent']
            del data_args['url']

            if not fs.is_dir(fs.path_join(data_args['destination'], data_args['name'])):
                self.log() and log.warn('Destination not exists. Skip')
                continue

            _args.update({  # re-init args
                'url': manga.url,
                **data_args,
            })
            provider = self._get_provider(_args)
            if provider:
                provider = provider()  # type Provider
                provider.before_provider(_args)
                provider.http.cookies = data.get('cookies')
                provider.http.ua = data.get('browser')
                provider.run(_args)
                provider.after_provider()
                provider.update_db()
                self.global_info.add_info(info)

    def _run_normal(self, _args, urls):
        for url in urls:
            _args['url'] = url
            provider = self._get_provider(_args)
            if provider:
                provider = provider()  # type Provider
                provider.before_provider(_args)
                provider.run(_args)
                provider.after_provider()
                provider.update_db()
                self.global_info.add_info(info)
