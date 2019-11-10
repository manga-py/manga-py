from argparse import ArgumentParser

from manga_py.meta import version


def _general_options(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('General options')

    args.add_argument('url', metavar='URL', type=str, nargs="*",
                      help='%(metavar)s, i.e. link from manga, to be downloaded.')

    args.add_argument('--version', action='version', version=version, help='Show %(prog)s version number and exit.')

    args.add_argument('-n', '--name', metavar='NAME', type=str, default='',
                      help='Rename manga, i.e. by %(metavar)s, and its folder to where it will be saved locally.')

    args.add_argument('-d', '--destination', metavar='PATH', type=str, default='Manga',
                      help='Destination folder to where the manga will be saved locally,'
                           ' i.e. `./%(metavar)s/manga_name/`.')

    args.add_argument('-P', '--no-progress', action='store_true', help='Don\'t show progress bar.')
