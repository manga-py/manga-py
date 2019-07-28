#!/usr/bin/python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from time import sleep


def main():
    import argcomplete
    import better_exceptions
    from requests.exceptions import ConnectionError
    from manga_py.libs.provider import Provider

    from . import cli
    argcomplete.autocomplete(cli.args.get_cli_arguments())
    # better_exceptions.hook()
    _cli = cli.Cli()
    try:
        check = _cli.check_version()
        if check['need_update']:
            cli.syslog('Please, update manga-py')
            cli.syslog('See url: %s\n' % check['url'])
            sleep(1)
    except ConnectionError:
        cli.syserr('Can\'t get manga-py version\n')
        sleep(1)
    _cli.run()


def db_main():
    import argcomplete
    import better_exceptions

    from .cli import db
    argcomplete.autocomplete(db.args())
    better_exceptions.hook()
    _db = db.DataBase()
    _db.run(db.args())
