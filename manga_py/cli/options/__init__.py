from argparse import ArgumentParser

from ._degug_options import debug_options
from ._download_options import downloading_options
from ._general_options import general_options
from ._images_options import images_options
from ._reader_options import reader_options


def parse_options(args_parser: ArgumentParser):
    general_options(args_parser)
    debug_options(args_parser)
    downloading_options(args_parser)
    images_options(args_parser)
    reader_options(args_parser)


__all__ = [
    'parse_options', 'general_options',
    'debug_options', 'downloading_options',
    'images_options', 'reader_options',
]

