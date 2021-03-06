import sys
from argparse import ArgumentParser
from getpass import getpass
from logging import error, warning
from os import name as os_name
from typing import Union

from progressbar import ProgressBar

from manga_py.fs import check_free_space, get_temp_path
from manga_py.parser import Parser


class Cli:  # pragma: no cover
    args = None
    parser = None
    _info = None
    __progress_bar = None

    def __init__(self, args: Union[dict, ArgumentParser], info=None):
        if type(args) == ArgumentParser:
            warning('args type of ArgumentParser deprecated. Please, use dict istread')
            args = args.parse_args().__dict__

        self.args = args
        self.parser = Parser(args)
        self._info = info

        space = self.args['min_free_space']
        if not check_free_space(get_temp_path(), space) or not check_free_space(self.args['destination'], space):
            raise OSError('No space left on device')

    def start(self):
        try:
            self.parser.init_provider(
                chapter_progress=self.chapter_progress,
                global_progress=self.global_progress,
                log=self.print,
                quest=self.quest,
                quest_password=self.quest_password,
                info=self._info,
            )
        except AttributeError as e:
            error('\n'.join([
                'Please check if your inputed domain is supported by manga-py: ',
                '- https://manga-py.com/manga-py/#resources-list',
                '- https://manga-py.github.io/manga-py/#resources-list (alternative)',
                'Make sure that your inputed URL is correct',
                'Trace:',
            ]))
            raise e

        self.parser.start()
        self.__progress_bar and self.__progress_bar.value > 0 and self.__progress_bar.finish()
        self.args['quiet'] or self.print(' ')

    def __init_progress(self, items_count: int, re_init: bool):
        if re_init or not self.__progress_bar:
            if re_init:
                self.__progress_bar.finish()

            bar = ProgressBar()
            self.__progress_bar = bar(range(items_count))
            self.__progress_bar.init()

    def chapter_progress(self, items_count: int, current_item: int, re_init: bool = False):
        if not items_count \
                or self.args['no_progress'] \
                or self.args['global_progress'] \
                or self.args['quiet'] \
                or self.args['print_json'] \
                or self.args['debug']:
            return

        self._progress(items_count, current_item, re_init)

    def global_progress(self, items_count: int, current_item: int, re_init: bool = False):
        if not items_count \
                or self.args['no_progress'] \
                or not self.args['global_progress'] \
                or self.args['quiet'] \
                or self.args['print_json'] \
                or self.args['debug']:

            return
        self._progress(items_count, current_item, re_init)

    def _progress(self, items_count: int, current_item: int, re_init: bool = False):
        current_val = 0

        if self.__progress_bar:
            current_val = self.__progress_bar.value

        self.__init_progress(items_count, re_init and current_val > 0)
        self.__progress_bar.update(current_item)

    def print(self, text, **kwargs):

        if os_name == 'nt':
            text = str(text).encode().decode(sys.stdout.encoding, 'ignore')

        self.args['quiet'] or print(text, **kwargs)

    def _single_quest(self, variants, title):
        print(title)

        for v in variants:
            print(v)

        return input()

    def _multiple_quest(self, variants, title):
        print(f'Accept - blank line + enter\n{title}')

        for v in variants:
            print(v)

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
