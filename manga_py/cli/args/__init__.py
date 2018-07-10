from argparse import ArgumentParser, Namespace
from . import _debug
from . import _downloading
from . import _general
from . import _image
from . import _reader


def get_cli_arguments() -> Namespace:
    """
    :return:
    :rtype Namespace
    """
    args_parser = ArgumentParser(add_help=False)

    _general.main(args_parser)
    _image.main(args_parser)
    _reader.main(args_parser)
    _downloading.main(args_parser)
    _debug.main(args_parser)

    args = args_parser.parse_args()
    return args
