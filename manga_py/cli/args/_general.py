from argparse import ArgumentParser


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('General options')

    args.add_argument('url', metavar='url', type=str, help='Downloaded url', nargs="+")

    args.add_argument('-n', '--name', metavar='name', type=str, help='Manga name', default='')
    args.add_argument('-d', '--destination', metavar='path', type=str,
                      help='Destination folder (Default = current directory', default='Manga')
    args.add_argument('-np', '--no-progress', metavar='no-progress', action='store_const',
                      const=True, help='Don\'t show progress bar', default=False)
