from argparse import ArgumentParser


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('General options')

    args.add_argument('url', metavar='url', type=str, help='Downloaded url(s)', nargs="*")

    args.add_argument('--title', type=str, default='',
                      help='Search manga from providers. (Not implemented now)')
    args.add_argument('-n', '--name', metavar='name', type=str, default=None,
                      help='Manga name (Works on one only url!)')
    args.add_argument('-d', '--destination', metavar='path', type=str, default='Manga',
                      help='Destination folder')
