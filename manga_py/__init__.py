#!/usr/bin/python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from sys import stderr
from time import sleep


def main():
    import argcomplete
    import better_exceptions
    from requests.exceptions import ConnectionError

    from .cli import Cli, args
    from .libs import print_lib
    argcomplete.autocomplete(args.get_cli_arguments())
    better_exceptions.hook()
    _cli = Cli()
    try:
        check = _cli.check_version()
        if check['need_update']:
            print_lib('Please, update manga-py')
            print_lib('See url: %s\n' % check['url'], file=stderr)
            sleep(1)
    except ConnectionError:
        print_lib('Can\'t get manga-py version\n', file=stderr)
    _cli.run()


def db_main():
    import argcomplete
    import better_exceptions

    from .cli import db
    argcomplete.autocomplete(db.args())
    better_exceptions.hook()
    _db = db.DataBase()
    _db.run(db.args())
