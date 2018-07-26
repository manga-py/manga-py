from argparse import ArgumentParser


def args():
    args_parser = ArgumentParser()
    args_parser.add_argument('--list', action='store_const', const=True,
                             help='Show all manga', default=False)
    args_parser.add_argument('-f', '--filter', metavar='name', type=str, help='Disable manga')
    args_parser.add_argument('-d', '--disable', metavar='id', type=int,
                             help='Disable manga (see manga ids from --list/filter)', default=0)
    args_parser.add_argument('-e', '--enable', metavar='id', type=int,
                             help='Enable manga (see manga ids from --list/filter)', default=0)
    args_parser.add_argument('--delete', metavar='id', type=int,
                             help='Delete manga (see manga ids from --list/filter)', default=0)
