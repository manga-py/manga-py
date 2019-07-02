import json
from datetime import datetime, timedelta
from sys import exit, stderr, stdout

from packaging import version
from requests import get

from . import args
from .. import meta
from ..libs import fs
from ..libs import print_lib
from ..libs.store import store
from .args.args_helper import ArgsListHelper

gh_check_file = fs.user_path().joinpath('github-check')


def _gh():
    with gh_check_file.open('w') as w:
        w.write(str(datetime.now().timestamp()))


class CliHelper:
    __slots__ = ('temp_path', 'raw_args', 'args')

    def __init__(self):
        self.temp_path = fs.temp_path()
        self.raw_args = args.get_cli_arguments()
        store.arguments = self.args = ArgsListHelper(self.raw_args)

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
        ok = {'message': 'Ok', 'need_update': False, 'tag': '', 'url': ''}
        if gh_check_file.is_file():  # check local file
            _date = None
            with gh_check_file.open('r') as r:
                _date = datetime.fromtimestamp(float(r.readline()))
                if _date + timedelta(days=1) < datetime.now():
                    return ok
        api_url = 'https://api.github.com/repos/%s/releases/latest' % meta.__repo_name__
        api_content = json.loads(get(api_url).text)
        tag_name = api_content['tag_name']
        if version.parse(tag_name) > version.parse(meta.__version__):
            download_addr = api_content['assets']
            if len(download_addr):
                url = download_addr[0]['browser_download_url']
            else:
                url = api_content['html_url']
            _gh()
            return {'message': 'Found new version', 'tag': tag_name, 'url': url, 'need_update': True}
        _gh()
        return ok

    def get_default_args(self):
        parser = self.raw_args
        all_defaults = {}
        for key in vars(args):
            all_defaults[key] = parser.get_default(key)
        return all_defaults