#!/usr/bin/python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from sys import stderr

import argcomplete
import better_exceptions

from .cli import Cli
from .cli import args, db


def main():
    argcomplete.autocomplete(args.get_cli_arguments())
    better_exceptions.hook()
    _cli = Cli()
    _cli.fill_args()
    check = _cli.check_version()
    if check['need_update']:
        print('Please, update manga-py')
        print('See url: %s' % check['url'], file=stderr)
    _cli.run()


def db_main():
    argcomplete.autocomplete(db.args())
    better_exceptions.hook()
    _db = db.DataBase()
    _db.run(db.args())
