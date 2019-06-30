from argparse import ArgumentParser


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('Reader options')

    args.add_argument('-C', '--cbz', action='store_true', help='Make *.cbz archives (for reader)')
    args.add_argument('-Z', '--zip', action='store_true', help='Make *.zip archives (for reader)')
    args.add_argument('-p', '--rename-pages', action='store_true',
                      help='Normalize images names. (example: 0_page_1.jpg -> 0001.jpg)')
    args.add_argument('-H', '--html', action='store_true', help='Generate html pages with image sliders')
