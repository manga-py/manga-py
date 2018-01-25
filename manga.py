#!/usr/bin/python3
# -*- coding: utf-8 -*-

from atexit import register as atexit_register
from os import makedirs
from os.path import isdir
from shutil import rmtree
from sys import argv, exit as sys_exit

from PyQt5.Qt import QApplication

from libs.cli import Cli, get_cli_arguments
from libs.fs import get_temp_path
from libs.gui import Gui

# from libs.server import Server

__author__ = 'Sergey Zharkov'
__license__ = 'MIT'
__email__ = 'sttv-pc@mail.ru'


def main():

    @atexit_register
    def before_shutdown():
        temp_dir = get_temp_path()
        isdir(temp_dir) and rmtree(temp_dir)

    temp_path = get_temp_path()
    isdir(temp_path) or makedirs(temp_path)

    args = get_cli_arguments()
    parse_args = args.parse_args()
    if parse_args.cli:
        cli = Cli(args)
        cli.start()
        exit(int(cli.status))

    # if parse_args.server:
    #     cli = Server(args)
    #     exit(0 if cli.status else 1)

    # else run GUI
    app = QApplication(argv)
    gui = Gui(args)
    gui.main()
    sys_exit(app.exec_())


if __name__ == '__main__':
    main()
