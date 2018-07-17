#!/usr/bin/python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from sys import stderr
try:
    import argcomplete
    from .cli import Cli
    from .cli import args

    argcomplete.autocomplete(args.get_cli_arguments())
except ImportError as e:
    print(e, file=stderr)


def main():
    _cli = Cli()
    _cli.fill_args()
    check = _cli.check_version()
    if check['need_update']:
        print('Please, update manga-py')
        print('See url: %s' % check['url'], file=stderr)
    _cli.run()


if __name__ == '__main__':
    main()
