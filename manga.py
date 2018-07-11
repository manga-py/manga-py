#!/usr/bin/python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from manga_py import main
from manga_py.cli.args import get_cli_arguments
import argcomplete


if __name__ == '__main__':
    argcomplete.autocomplete(get_cli_arguments())
    main()
