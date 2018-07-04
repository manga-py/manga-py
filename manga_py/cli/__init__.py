import json
import sys
from argparse import ArgumentParser
from os import name as os_name
from getpass import getpass

import requests
from packaging import version
from progressbar import ProgressBar

from manga_py.meta import __version__, __repo_name__
from manga_py.parser import Parser


def check_version():
    api_url = 'https://api.github.com/repos/%s/releases/latest' % __repo_name__
    api_content = json.loads(requests.get(api_url).text)
    tag_name = api_content['tag_name']
    if version.parse(tag_name) > version.parse(__version__):
        download_addr = api_content['assets']
        if len(download_addr):
            url = download_addr[0]['browser_download_url']
        else:
            url = api_content['html_url']
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
        try:
            self.parser.init_provider(
                progress=self.progress,
                log=self.print,
                quest=self.quest,
                quest_password=self.quest_password,
                info=self._info,
            )
        except AttributeError as e:
            print(e)
            print('Please check the domain in the table: https://manga-dl.yuru-yuri.sttv.me')
            print('Make sure that the URL is correct\n')
            raise e
        self.parser.start()
        self.__progress_bar and self.__progress_bar.value > 0 and self.__progress_bar.finish()
        self.print(' ')

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
        return input()

    def _multiple_quest(self, variants, title):
        self.print('Accept - blank line + enter')
        self.print(title)
        for v in variants:
            self.print(v)
        result = []
        while True:
            _ = input().strip()
            if not len(_):
                return result
            result.append(_)

    def quest(self, variants: enumerate, title: str, select_type=0):  # 0 = single, 1 = multiple
        if select_type:
            return self._multiple_quest(variants, title)
        return self._single_quest(variants, title)

    def quest_password(self, title):
        return getpass(title)
