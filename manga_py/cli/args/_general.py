from argparse import ArgumentParser


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('General options')

    args.add_argument('url', metavar='url', type=str, help='Downloaded url(s)', nargs="*")

    args.add_argument('--title', type=str, default='',
                      help='Search manga from providers. (Not implemented now)')
    args.add_argument('-n', '--name', metavar='name', type=str,
                      help='Manga name (Works on one only url!)', default=None)
    args.add_argument('-d', '--destination', metavar='path', type=str,
                      help='Destination folder', default='Manga')
