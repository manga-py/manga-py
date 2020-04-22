#!/usr/bin/python3
# -*- coding: utf-8 -*-

import traceback
from atexit import register as atexit_register
from json import dumps
from os import makedirs, path
from shutil import rmtree
from sys import exit, stderr
from logging import info, warning, basicConfig, DEBUG, WARN

import better_exceptions

better_exceptions.hook()


display, driver = None, None


@atexit_register
def before_shutdown():
    from .fs import get_temp_path
    from .base_classes.web_driver import display, driver

    display and display.stop()
    driver and driver.close()
    temp_dir = get_temp_path()
    path.isdir(temp_dir) and rmtree(temp_dir)


def _run_util(args):
    """
    :param args:
    :return:
    :rtype Info|str
    """
    from .info import Info
    parse_args = args.parse_args()
    _info = Info(parse_args)

    from .cli import Cli
    _info.start()
    Cli(args, _info).start()

    if parse_args.print_json:
        _info = dumps(
            _info.get(),
            indent=2,
        )
    else:
        _info = []

    return _info


def _update_all(args):
    from .fs import get_info
    parse_args = args.parse_args()
    info('Update all')
    multi_info = {}

    dst = parse_args.destination
    json_info = get_info(dst)

    for i in json_info:
        parse_args.manga_name = i['manga_name']
        parse_args.url = i['url']
        _info = _run_util(args)
        multi_info[i['directory']] = _info
    parse_args.quiet or (parse_args.print_json and print(multi_info))


def run_util(args):
    from .fs import get_temp_path

    temp_path = get_temp_path()
    path.isdir(temp_path) or makedirs(temp_path)

    parse_args = args.parse_args()

    try:
        _info = _run_util(args)
        parse_args.quiet or (parse_args.print_json and print(_info))
    except KeyboardInterrupt:
        warning('\nUser interrupt')


def main():
    from .cli.args import get_cli_arguments
    args = get_cli_arguments()

    log_format = '"%(levelname)s:%(pathname)s:%(lineno)s:%(asctime)s:%(message)s"'
    basicConfig(level=(DEBUG if args.parse_args().debug else WARN), format=log_format)

    from .meta import _version

    if ~_version.find('alpha'):
        warning('Alpha release! There may be errors!')

    exit(run_util(args))


if __name__ == '__main__':
    main()
