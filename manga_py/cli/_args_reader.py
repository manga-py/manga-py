
def _args_reader(args_parser):  # pragma: no cover
    args = args_parser.add_argument_group('Archive options')

    args.add_argument(
        '-z',
        '--cbz',
        action='store_true',
        help=(
            'Make `*.cbz` archives (for reader).'
        )
    )

    args.add_argument(
        '-R',
        '--rename-pages',
        action='store_true',
        help=(
            'Normalize image filenames. '
            'E.g. from `0_page_1.jpg` to `0001.jpg`.'
        )
    )
