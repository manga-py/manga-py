#!/usr/bin/python3
# -*- coding: utf-8 -*-

from libs.cli import Cli
from libs.parser import Parser

if __name__ == '__main__':
    parser = Parser()
    args = Cli.get_arguments()
    if args.parse_args().cli:
        cli = Cli(parser, args)
        # cli
        exit(cli.status)


    print(args.parse_args().name)
