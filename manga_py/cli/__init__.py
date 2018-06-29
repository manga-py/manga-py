import atexit
from getpass import getpass
from shutil import rmtree
from sys import stderr

import better_exceptions
from progressbar import ProgressBar
from zenlog import log

from manga_py.cli.args import get_cli_arguments
from manga_py.libs.fs import get_temp_path, make_dirs
from manga_py.libs.info import Info
from manga_py.libs.providers import get_provider


class Cli:
    info = None
    _temp_path = None

    def __init__(self):
        atexit.register(self.exit)
        self._temp_path = get_temp_path()
        make_dirs(self._temp_path)

    def exit(self):
        # remove temp directory
        rmtree(self._temp_path)

    @classmethod
    def print_error(cls, *args):
        print(*args, file=stderr)

    def run(self):
        better_exceptions.hook()
        args = get_cli_arguments()
        self.info = Info(args)
        urls = args.get('url', [])

        for url in urls:
            provider = get_provider(url)
            provider.print = print
            provider.print_error = self.print_error
            provider.input = input
            provider.password = getpass
            provider.logger = log
            provider.info = self.info
            provider.progressbar = ProgressBar
            provider.run(args)

    # @classmethod
    # def check_version(cls):
    #     api_url = 'https://api.github.com/repos/%s/releases/latest' % meta.__repo_name__
    #     api_content = json.loads(Http().get(api_url).text)
    #     tag_name = api_content['tag_name']
    #     if version.parse(tag_name) > version.parse(meta.__version__):
    #         download_addr = api_content['assets']
    #         if len(download_addr):
    #             url = download_addr[0]['browser_download_url']
    #         else:
    #             url = api_content['html_url']
    #         return {'message': 'Found new version', 'tag': tag_name, 'url': url, 'need_update': True}
    #     return {'message': 'Ok', 'need_update': False, 'tag': '', 'url': ''}
