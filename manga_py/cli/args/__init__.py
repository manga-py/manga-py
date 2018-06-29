from argparse import ArgumentParser
from . import _debug
from . import _downloading
from . import _general
from . import _image
from . import _reader


def get_cli_arguments(as_dict=True) -> dict:
    args_parser = ArgumentParser(add_help=False)

    _general.main(args_parser)
    _image.main(args_parser)
    _reader.main(args_parser)
    _downloading.main(args_parser)
    _debug.main(args_parser)

    args = args_parser.parse_args()
    return args.__dict__ if as_dict else args
