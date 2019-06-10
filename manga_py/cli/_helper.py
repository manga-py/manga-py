import json
# from getpass import getpass
from sys import exit, stderr, stdout

from packaging import version

from manga_py import meta
from manga_py.cli import args
from manga_py.libs import fs
from requests import get
from .args import ArgsListHelper
from manga_py.libs import print_lib


class CliHelper:
    __slots__ = ('temp_path', 'raw_args', 'args')

    def __init__(self):
        self.temp_path = fs.get_temp_path()
        self.raw_args = args.get_cli_arguments()
        self.args = ArgsListHelper(self.raw_args)

    def show_log(self) -> bool:
        return self.args.get('show-log') or self.args.get('verbose-log')

    @classmethod
    def print(cls, *_args):
        print_lib(*_args, file=stdout)

    @classmethod
    def print_error(cls, *_args):
        print_lib(*_args, file=stderr)

    def _print_cli_help(self):
        if len(self.args.get('url')) < 1 and not self.args.get('update_all'):
            self.raw_args.print_help()
            exit()

    @classmethod
    def check_version(cls):
        api_url = 'https://api.github.com/repos/%s/releases/latest' % meta.__repo_name__
        api_content = json.loads(get(api_url).text)
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
        parser = self.raw_args
        all_defaults = {}
        for key in vars(args):
            all_defaults[key] = parser.get_default(key)
        return all_defaults
