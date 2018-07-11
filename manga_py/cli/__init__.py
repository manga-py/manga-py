import atexit
import json
from getpass import getpass
from shutil import rmtree
from sys import stderr

import better_exceptions
from packaging import version
from progressbar import ProgressBar
from zenlog import log

from manga_py import meta
from manga_py.cli import args
from manga_py.libs import print_lib
from manga_py.libs.fs import get_temp_path, make_dirs
from manga_py.libs.http import Http
from manga_py.libs.info import Info
from manga_py.libs.providers import get_provider


class Cli:
    info = None
    _temp_path = None
    _args = None
    __raw_args = None

    def __init__(self):
        self._temp_path = get_temp_path()
        atexit.register(self.exit)
        make_dirs(self._temp_path)

    def exit(self):
        # remove temp directory
        rmtree(self._temp_path)

    @classmethod
    def print_error(cls, *_args):
        print_lib(*_args, file=stderr)

    def _print_cli_help(self):
        if len(self._args.get('url')) < 1 and not self._args.get('update_all'):
            self.__raw_args.print_help()

    def fill_args(self):
        self.__raw_args = args.get_cli_arguments()
        self._args = args.arguments_to_dict(self.__raw_args)

    def run(self):
        better_exceptions.hook()
        _args = self._args.copy()
        self._print_cli_help()
        self.info = Info(_args)
        urls = _args.get('url', []).copy()

        if len(urls) > 1:
            _args['name'] = None

        for url in urls:
            provider = get_provider(url)

            provider.print = print_lib
            provider.print_error = self.print_error
            provider.input = input
            provider.password = getpass
            provider.logger = log
            provider.info = self.info
            provider.progressbar = ProgressBar

            _args['url'] = url

            provider.run(_args)

    @classmethod
    def check_version(cls):
        api_url = 'https://api.github.com/repos/%s/releases/latest' % meta.__repo_name__
        api_content = json.loads(Http().get(api_url).text)
        tag_name = api_content['tag_name']
        if version.parse(tag_name) > version.parse(meta.__version__):
            download_addr = api_content['assets']
            if len(download_addr):
                url = download_addr[0]['browser_download_url']
            else:
                url = api_content['html_url']
            return {'message': 'Found new version', 'tag': tag_name, 'url': url, 'need_update': True}
        return {'message': 'Ok', 'need_update': False, 'tag': '', 'url': ''}
