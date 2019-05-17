import atexit
import json
from shutil import rmtree

from manga_py.libs.log import logger as log

from manga_py.libs.info.glob import InfoGlobal
from manga_py.libs.info import Info
from . import args
from ._helper import CliHelper
from .db import DataBase
from manga_py.libs import fs


class Cli(CliHelper):
    __slots__ = ()
    db = DataBase()
    info = InfoGlobal()

    def __init__(self):
        atexit.register(self.exit)

    def exit(self):
        # remove temp directory
        rmtree(self._temp_path)

    def run(self):
        _args = self._args.copy()
        if _args.get('title'):  # todo: Maybe search for user-urls only
            urls = self._search_for_title(_args.get('title'))
        else:
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
        for manga in self.db.get_all():  # type: Manga
            self.show_log() and log.info('Update %s', manga.url)
            _args = default_args.copy()
            data = json.loads(manga.data)
            data_args = data.get('args', {})
            del data_args['rewrite_exists_archives']
            del data_args['user_agent']
            del data_args['url']

            if not fs.is_dir(fs.path_join(data_args['destination'], data_args['name'])):
                self.show_log() and log.warn('Destination not exists. Skip')
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
                self.show_log() and log.error('Provider not exists')

    def _run_normal(self, _args, urls):
        for url in urls:
            _args['url'] = url
            provider = self._get_provider(_args)  # type: Provider
            if provider:
                provider.before_provider(_args)
                provider.run(_args)
                provider.after_provider()
                provider.update_db()
                self.global_info.add_info(info)
            else:
                self.show_log() and log.warn('Provider not exists')
