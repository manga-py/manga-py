from argparse import ArgumentParser


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('Authentication')

    args.add_argument('--login', type=str, default=None, help='Authentication login')
    args.add_argument('--password', type=str, default=None, help='Authentication password')
    args.add_argument('--cookies', type=str, default=[], nargs='*',
                      help='Authentication cookies (if need)\n\tExample: --cookies ga=ca.ca.d tz=412')
