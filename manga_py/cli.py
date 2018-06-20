import json
import sys
from argparse import ArgumentParser
from os import name as os_name

import requests
from packaging import version
from progressbar import ProgressBar

from .meta import __version__, __repo_name__
from .parser import Parser


def _image_args(args_parser):
    args = args_parser.add_argument_group('Image options')

    args.add_argument('--not-change-files-extension', action='store_const',
                      help='Save files to archive "as is"', const=True, default=False)

    # args.add_argument('--force-png', action='store_const', 
    #                          help='Force conversation images to png format', const=True, default=False)
    # args.add_argument('--force-jpg', action='store_const', 
    #                          help='Force conversation images to jpg format', const=True, default=False)

    # args.add_argument('-xt', type=int, help='Manual image crop with top side', default=0)
    # args.add_argument('-xr', type=int, help='Manual image crop with right side', default=0)
    # args.add_argument('-xb', type=int, help='Manual image crop with bottom side', default=0)
    # args.add_argument('-xl', type=int, help='Manual image crop with left side', default=0)
    # args.add_argument('--crop-blank', action='store_const', help='Crop white lines on image',
    #                          const=True, default=False)


def _debug_args(args_parser):
    args = args_parser.add_argument_group('Debug / Simulation options')

    args.add_argument('-h', '--help', action='help', help='show help and exit')
    args.add_argument('--print-json', action='store_const', const=True, default=False,
                      help='Print information about the results in the form of json (after completion)' +
                      ' - Not worked now')

    args.add_argument('--simulate', action='store_const', const=True, default=False,
                      help='Do not download the files and do not write anything to disk' +
                      ' - Not worked now')

    # args.add_argument('-vv', '--log', metavar='info', type='str', help='Verbose log')


def _downloading_args(args_parser):
    args = args_parser.add_argument_group('Downloading options')

    args.add_argument('-s', '--skip-volumes', metavar='count', type=int,
                      help='Skip volumes', default=0)
    args.add_argument('-c', '--max-volumes', metavar='count', type=int,
                      help='Maximum volumes for downloading 0=All', default=0)
    args.add_argument('--user-agent', type=str, help='Don\'t work from protected sites')
    args.add_argument('--proxy', type=str, help='Http proxy')
    args.add_argument('--reverse-downloading', action='store_const',
                      help='Reverse volumes downloading', const=True, default=False)
    args.add_argument('--rewrite-exists-archives', action='store_const', const=True,
                      default=False)
    args.add_argument('-nm', '--no-multi-threads', action='store_const',
                      help='Disallow multi-threads images downloading', const=True, default=False)
    args.add_argument('--zero-fill', action='store_const', const=True, default=False,
                      help='Adds 0 to the end for all chapters (vol_001.zip -> vol_001-0.zip)')


def _reader_args(args_parser):
    args = args_parser.add_argument_group('Archive options')

    args.add_argument('--cbz', action='store_const', default=False,
                      const=True, help='Make *.cbz archives (for reader)')

    args.add_argument('--rename-pages', action='store_const', default=False, const=True,
                      help='Normalize images names. (example: 0_page_1.jpg -> 0001.jpg)')


def get_cli_arguments() -> ArgumentParser:  # pragma: no cover
    args_parser = ArgumentParser(add_help=False)
    args = args_parser.add_argument_group('General options')

    args.add_argument('url', metavar='url', type=str, help='Downloaded url')
    args.add_argument('--version', action='version', version=__version__)

    args.add_argument('-n', '--name', metavar='name', type=str, help='Manga name', default='')
    args.add_argument('-d', '--destination', metavar='destination', type=str,
                      help='Destination folder (Default = current directory')
    args.add_argument('-np', '--no-progress', metavar='no-progress', action='store_const',
                      const=True, help='Don\'t show progress bar', default=False)
    # future
    # args_parser.add_argument('--server', action='store_const', const=True, help='Run web interface',
    #                          default=False)

    _image_args(args_parser)
    _reader_args(args_parser)
    _downloading_args(args_parser)
    _debug_args(args_parser)

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
    args = None
    parser = None
    _info = None
    __progress_bar = None

    def __init__(self, args: ArgumentParser, info=None):
        self.args = args.parse_args()
        self.parser = Parser(args)
        self._info = info

    def start(self):
        self.parser.init_provider(
            progress=self.progress,
            log=self.print,
            quest=self.quest,
            info=self._info,
        )
        self.parser.start()
        self.__progress_bar and self.__progress_bar.value > 0 and self.__progress_bar.finish()
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
        if not self.args.no_progress and not self.args.print_json:
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
