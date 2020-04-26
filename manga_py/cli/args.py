"""
manga-py module for CLI and its options.
"""

import os
from argparse import ArgumentParser, MetavarTypeHelpFormatter

from manga_py.meta import version
from ._args_debug import _args_debug
from ._args_downloading import _args_downloading
from ._args_general import _args_general
from ._args_image import _args_image
from ._args_reader import _args_reader


class Formatter(MetavarTypeHelpFormatter):
    def __init__(self, prog, indent_increment=2, max_help_position=30, width=None):
        if width is None:
            try:
                width = int(os.environ['COLUMNS'])
            except (KeyError, ValueError):
                width = 100
        super().__init__(prog, indent_increment, max_help_position, width)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                args_len = len(action.option_strings) - 1
                for i, option_string in enumerate(action.option_strings):
                    if i == args_len:
                        parts.append('%s %s' % (option_string, args_string))
                    else:
                        parts.append(option_string)
            return ', '.join(parts)


def get_cli_arguments() -> ArgumentParser:  # pragma: no cover
    """
    Method to generate manga-py CLI with its options.
    """
    args_parser = ArgumentParser(
        add_help=False,
        formatter_class=Formatter,
        prog="manga-py",
        description=(
            '%(prog)s is the universal manga downloader (for your offline reading).\n  '
            'Site: https://manga-py.com/manga-py/\n  '
            'Source-code: https://github.com/manga-py/manga-py\n  '
            'Version: ' + version
        ),
        epilog=(
            'So, that is how %(prog)s can be executed to download yours favourite mangas.\n'
            'Enjoy! 😉'
        )
    )

    _args_general(args_parser, version)
    _args_downloading(args_parser)
    _args_reader(args_parser)
    _args_image(args_parser)
    _args_debug(args_parser)

    return args_parser
