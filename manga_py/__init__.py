#!/usr/bin/python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from sys import stderr
from time import sleep

import argcomplete
import better_exceptions

from manga_py.cli import Cli, args, db
from manga_py.libs import print_lib


def main():
    argcomplete.autocomplete(args.get_cli_arguments())
    better_exceptions.hook()
    _cli = Cli()
    try:
        check = _cli.check_version()
        if check['need_update']:
            print_lib('Please, update manga-py')
            print_lib('See url: %s\n' % check['url'], file=stderr)
            sleep(1)
    except Exception:
        print_lib('Can\'t get manga-py version\n', file=stderr)
    _cli.run()


def db_main():
    argcomplete.autocomplete(db.args())
    better_exceptions.hook()
    _db = db.DataBase()
    _db.run(db.args())
