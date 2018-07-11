#!/usr/bin/python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

try:
    import argcomplete
    from .cli import Cli
    from .cli import args
    from sys import stderr

    argcomplete.autocomplete(args.get_cli_arguments())
except ImportError as e:
    print(e, file=stderr)


def main():
    _cli = Cli()
    check = _cli.check_version()
    if check['need_update']:
        print('See url: %s' % check['url'], file=stderr)
    _cli.run()


if __name__ == '__main__':
    main()
