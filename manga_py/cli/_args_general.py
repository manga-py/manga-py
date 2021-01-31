from argparse import ArgumentParser


def _args_general(args_parser: ArgumentParser, version):  # pragma: no cover
    args = args_parser.add_argument_group('General options')

    args.add_argument(
        'url',
        metavar='URL',
        type=str,
        help=(
            '%(metavar)s, i.e. link from manga, to be downloaded.'
        )
    )

    args.add_argument(
        '-v',
        '--version',
        action='version',
        version=version,
        help=(
            'Show %(prog)s\'s version number and exit.'
        )
    )

    args.add_argument(
        '-n',
        '--name',
        metavar='NAME',
        type=str,
        default='',
        help=(
            'Rename manga, i.e. by %(metavar)s, and its folder to where it will be saved locally.'
        )
    )

    args.add_argument(
        '-d',
        '--destination',
        metavar='PATH',
        type=str,
        default='Manga',
        help=(
            'Destination folder to where the manga will be saved locally. '
            'The path will be `./%(metavar)s/manga_name/`.'
        )
    )

    args.add_argument(
        '-P',
        '--no-progress',
        action='store_true',
        help=(
            'Don\'t show progress bar.'
        )
    )

    args.add_argument(
        '--global-progress',
        action='store_true',
        help=(
            'Show a global progress bar instead of a file-by-file progress.'
        )
    )

    args.add_argument(
        '--arguments',
        type=str,
        nargs='*',
        help=(
            '!!!WARNING!!! This option in-debug mode'
            'An arbitrary set of arguments that can be used in the provider. '
            'If you need to transfer login, you can do it here. (--arguments login=my-login password=my-pasword) '
            'If the provider requires a language choice, you can pass it (--arguments language=my-language) '
            'If site have multiple translators groups, manga-py can try download only specified translator: '
            ' (--arguments translator=awesome-translator) '
        )
    )

