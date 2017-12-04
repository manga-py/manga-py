#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Sergey Zharkov'
__license__ = 'MIT'
__email__ = 'sttv-pc@mail.ru'
__version__ = '0.3.0'
__downloader_uri__ = 'https://github.com/yuru-yuri/Manga-Downloader'

from sys import argv, exit as sys_exit
from libs.cli import Cli, get_cli_arguments
from libs.gui import Gui
from PyQt5.Qt import QApplication
from libs.parser import Parser
from os.path import isdir
from os import makedirs
from libs import fs

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
