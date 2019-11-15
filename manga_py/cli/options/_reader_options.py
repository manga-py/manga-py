from argparse import ArgumentParser


def reader_options(args_parser: ArgumentParser):  # pragma: no cover
    args = args_parser.add_argument_group('Reader options')

    args.add_argument('--cbz', action='store_true',
                      help='Make `*.cbz` archives (for reader). Default extension is `*.zip`')

    args.add_argument('-A', '--no-archive', action='store_true',
                      help='Don\'t make archive (save files in folders)')

    args.add_argument('--rename-pages', action='store_true',
                      help='Normalize image filenames. E.g. from `0_page_1.jpg` to `001.jpg`.')


__all__ = ['reader_options']
