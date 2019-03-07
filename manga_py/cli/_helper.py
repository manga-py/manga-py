import json
from getpass import getpass
from sys import exit, stderr

from packaging import version
from progressbar import ProgressBar
from zenlog import log

from manga_py import meta
from manga_py.cli import args
from manga_py.provider import Provider
from manga_py.libs import print_lib
from manga_py.libs.http import Http
from manga_py.libs.modules import info
from manga_py.providers import get_provider


class CliHelper:
    __raw_args = None
    _temp_path = None
    _args = None
    global_info = None

    def show_log(self) -> bool:
        return self._args.get('show-log') or self._args.get('verbose-log')

    @classmethod
    def print_error(cls, *_args):
        print_lib(*_args, file=stderr)

    def _print_cli_help(self):
        if len(self._args.get('url')) < 1 and not self._args.get('update_all'):
            self.__raw_args.print_help()
            exit()

    def fill_args(self):
        self.__raw_args = args.get_cli_arguments()
        self._args = args.arguments_to_dict(self.__raw_args)

    def _get_provider(self, _args, provider=None):
        local_info = info.Info(_args)
        if provider is None:
            try:
                provider = get_provider(_args['url'])
            except ImportError as e:
                self.global_info.add_info(info, self.global_info.ERROR, e)
                self.show_log() and log.err(e)
                return
        provider = provider()  # type: Provider
        provider.set_callbacks(
            print=print_lib,
            print_error=self.print_error,
            input=input,
            password=getpass,
            logger=log,
            info=local_info,
            progressbar=ProgressBar,
        )
        return provider

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

    def get_default_args(self):
        parser = self.__raw_args
        all_defaults = {}
        for key in vars(args):
            all_defaults[key] = parser.get_default(key)
        return all_defaults

    def _search_for_title(self, title):
        if len(title) < 1:
            raise ValueError('Title is empty!')

        raise UserWarning('Not implemented now')
