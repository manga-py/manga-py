

def _args_debug(args_parser):  # pragma: no cover
    args = args_parser.add_argument_group('Debug / Simulation options')

    args.add_argument(
        '-h',
        '--help',
        action='help',
        help=(
            'Show this help and exit.'
        )
    )

    args.add_argument(
        '--print-json',
        action='store_true',
        help=(
            'Print information about the results in the JSON format (after completion).'
        )
    )

    args.add_argument(
        '--simulate',
        action='store_true',
        help=(
            'Simulate running %(prog)s, where: '
            '1) do not download files and, '
            '2) do not write anything on disk.'
        )
    )

    # deprecated
    args.add_argument(
        '--show-current-chapter-info',
        action='store_true',
        help=(
            'Show current processing chapter info.'
        )
    )

    # deprecated
    args.add_argument(
        '--save-current-chapter-info',
        action='store_true',
        help=(
            'Save current processing chapter info into a JSON file.'
        )
    )

    args.add_argument(
        '--show-chapter-info',
        action='store_true',
        help=(
            'Show current processing chapter info.'
        )
    )

    args.add_argument(
        '--save-chapter-info',
        action='store_true',
        help=(
            'Save current processing chapter info into a JSON file.'
        )
    )

    args.add_argument(
        '--save-manga-info',
        action='store_true',
        help=(
            'Saves the manga data in a into a JSON file at the root of the download folder.'
        )
    )

    args.add_argument(
        '--debug',
        action='store_true',
        help=(
            'Debug %(prog)s.'
        )
    )

    args.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help=(
            'Dont show any messages.'
        )
    )
