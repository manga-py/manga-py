from argparse import ArgumentParser


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('Authentication')

    args.add_argument('--login', type=str, default=None, help='Authentication login')
    args.add_argument('--password', type=str, default=None, help='Authentication password')
    args.add_argument('-A', '--dont-save-cookies', action='store_true',
                      help='Don\'t allow save cookies. Important! Cookies required for --update-all option!')
