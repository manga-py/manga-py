#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import makedirs
from os.path import isdir
from sys import argv, exit as sys_exit

from PyQt5.Qt import QApplication

from libs import fs
from libs.cli import Cli, get_cli_arguments, __version__ as __version
from libs.gui import Gui
from libs.parser import Parser

__author__ = 'Sergey Zharkov'
__license__ = 'MIT'
__email__ = 'sttv-pc@mail.ru'
__version__ = __version

if __name__ == '__main__':

    temp_path = fs.get_temp_path()
    isdir(temp_path) or makedirs(temp_path)

    parser = Parser()
    args = get_cli_arguments()
    parse_args = args.parse_args()
    if parse_args.cli:
        cli = Cli(parser, args)
        # cli
        exit(cli.status)

    # else run GUI
    app = QApplication(argv)
    gui = Gui(parser, args)
    gui.main()
    sys_exit(app.exec_())
