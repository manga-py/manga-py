from argparse import ArgumentParser


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('General options')

    args.add_argument('url', metavar='url', type=str, help='Downloaded url(s)', nargs="*")

    args.add_argument('-n', '--name', metavar='name', type=str, help='Manga name', default=None)
    args.add_argument('-d', '--destination', metavar='path', type=str, default='Manga',
                      help='Destination folder (Default = current directory')
