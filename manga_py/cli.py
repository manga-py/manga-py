import json
import sys
from argparse import ArgumentParser
from os import name as os_name

import requests
from packaging import version
from progressbar import ProgressBar

from manga_py.parser import Parser
from manga_py.meta import __version__, __repo_name__


def _image_args(args_parser):
    # args_parser.add_argument('--force-png', action='store_const', required=False,
    #                          help='Force conversation images to png format', const=True, default=False)
    # args_parser.add_argument('--force-jpg', action='store_const', required=False,
    #                          help='Force conversation images to jpg format', const=True, default=False)

    args_parser.add_argument('-xt', required=False, type=int, help='Manual image crop with top side', default=0)
    args_parser.add_argument('-xr', required=False, type=int, help='Manual image crop with right side', default=0)
    args_parser.add_argument('-xb', required=False, type=int, help='Manual image crop with bottom side', default=0)
    args_parser.add_argument('-xl', required=False, type=int, help='Manual image crop with left side', default=0)
    args_parser.add_argument('--crop-blank', action='store_const', required=False, help='Crop white lines on image',
                             const=True, default=False)


def _downloading_args(args_parser):
    args_parser.add_argument('-s', '--skip-volumes', metavar='skip-volumes', type=int, required=False,
                             help='Skip volumes (count)', default=0)
    args_parser.add_argument('-c', '--max-volumes', metavar='max-volumes', type=int, required=False,
                             help='Maximum volumes for downloading 0=All (count)', default=0)
    args_parser.add_argument('--user-agent', required=False, type=str, help='Don\'t work from protected sites',
                             default=None)
    args_parser.add_argument('--proxy', required=False, type=str, help='Http proxy', default=None)
    args_parser.add_argument('--reverse-downloading', action='store_const', required=False,
                             help='Reverse volumes downloading', const=True, default=False)
    args_parser.add_argument('--rewrite-exists-archives', action='store_const', required=False, const=True,
                             default=False)
    args_parser.add_argument('-nm', '--no-multi-threads', action='store_const', required=False,
                             help='Disallow multi-threads images downloading', const=True, default=False)


def get_cli_arguments() -> ArgumentParser:  # pragma: no cover
    args_parser = ArgumentParser()

    args_parser.add_argument('url', metavar='url', type=str, help='Downloaded url', default='', nargs='?')
    args_parser.add_argument('--version', action='version', version=__version__)

    args_parser.add_argument('-n', '--name', metavar='name', type=str, required=False, help='Manga name', default='')
    args_parser.add_argument('-d', '--destination', metavar='destination', type=str, required=False,
                             help='Destination folder (Default = current directory', default='')
    # args_parser.add_argument('-vv', '--log', metavar='info', action='store_const', required=False, const=True,
    #                          default=False, help='Verbose log')
    # args_parser.add_argument('-vvv', '--verbose-log', metavar='verbose_info', action='store_const', required=False,
    #                          const=True, default=False, help='Verbose log')
    args_parser.add_argument('-np', '--no-progress', metavar='no-progress', action='store_const', required=False,
                             const=True, help='Don\'t show progress bar', default=False)
    # future
    # args_parser.add_argument('--server', action='store_const', required=False, const=True, help='Run web interface',
    #                          default=False)

    _image_args(args_parser)
    _downloading_args(args_parser)

    return args_parser


def check_version():
    api_url = 'https://api.github.com/repos/%s/releases/latest' % __repo_name__
    api_content = json.loads(requests.get(api_url).text)
    tag_name = api_content['tag_name']
    if version.parse(tag_name) > version.parse(__version__):
        download_addr = api_content['assets'][0]
        url = download_addr['browser_download_url']
        return {'message': 'Found new version', 'tag': tag_name, 'url': url, 'need_update': True}
    return {'message': 'Ok', 'need_update': False, 'tag': '', 'url': ''}


class Cli:
    status = True
    args = None
    parser = None
    __progress_bar = None

    def __init__(self, args: ArgumentParser):
        self.args = args.parse_args()
        self.parser = Parser(args)

    def start(self):
        self.parser.init_provider(
            progress=self.progress,
            log=self.print,
            quest=self.quest,
        )
        self.parser.start()
        self.print(' ')

    def input(self, prompt: str = ''):
        return input(prompt=prompt + '\n')

    def __init_progress(self, items_count: int, re_init: bool):
        if re_init or not self.__progress_bar:
            if re_init:
                print(' ')
                self.__progress_bar.finish()
            bar = ProgressBar()
            self.__progress_bar = bar(range(items_count))
            self.__progress_bar.init()

    def progress(self, items_count: int, current_item: int, re_init: bool = False):
        if not items_count:
            return
        if not self.args.no_progress:
            current_val = 0
            if self.__progress_bar:
                current_val = self.__progress_bar.value
            self.__init_progress(items_count, re_init and current_val > 0)
            self.__progress_bar.update(current_item)

    def print(self, text, end='\n'):
        if os_name == 'nt':
            text = str(text).encode().decode(sys.stdout.encoding, 'ignore')
        print(text, end=end)

    def _single_quest(self, variants, title):
        self.print(title)
        for v in variants:
            self.print(v)
        return self.input()

    def _multiple_quest(self, variants, title):
        self.print('Accept - blank line + enter')
        self.print(title)
        for v in variants:
            self.print(v)
        result = []
        while True:
            _ = self.input().strip()
            if not len(_):
                return result
            result.append(_)

    def quest(self, variants: enumerate, title: str, select_type=0):  # 0 = single, 1 = multiple
        if select_type:
            return self._multiple_quest(variants, title)
        return self._single_quest(variants, title)
