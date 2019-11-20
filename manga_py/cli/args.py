'''
manga-py module for CLI and its options.
'''

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter

from manga_py.meta import __version__


class DescriptionDefaultsHelpFormatter(ArgumentDefaultsHelpFormatter,
                                       RawDescriptionHelpFormatter):
    '''
    Class to format --help cli option with 2 features to output:
        programm's description in a raw mode,
        options default values.
    '''


def _image_args(args_parser):  # pragma: no cover
    args = args_parser.add_argument_group('Image options')

    args.add_argument(
        '-E',
        '--not-change-files-extension',
        action='store_true',
        help=(
            'Save downloaded files to archive "as is".'
        )
    )

    args.add_argument(
        '-W',
        '--no-webp',
        action='store_true',
        help=(
            'Convert `*.webp` images to `*.jpg` format.'
        )
    )


def _debug_args(args_parser):  # pragma: no cover
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
        '-j',
        '--print-json',
        action='store_true',
        help=(
            'Print information about the results in the JSON format (after completion).'
        )
    )

    args.add_argument(
        '-l',
        '--simulate',
        action='store_true',
        help=(
            'Simulate running %(prog)s, where: '
            '1) do not download files and, '
            '2) do not write anything on disk.'
        )
    )

    args.add_argument(
        '-i',
        '--show-current-chapter-info',
        action='store_true',
        help=(
            'Show current processing chapter info.'
        )
    )

    args.add_argument(
        '-b',
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


def _downloading_args(args_parser):  # pragma: no cover
    args = args_parser.add_argument_group('Downloading options')

    args.add_argument(
        '-s',
        '--skip-volumes',
        metavar='COUNT',
        type=int,
        help=(
            'Skip a total number, i.e. %(metavar)s, of volumes.'
        ),
        default=0
    )

    args.add_argument(
        '-m',
        '--max-volumes',
        metavar='COUNT',
        type=int,
        default=0,
        help=(
            'Download a maximum number, i.e. %(metavar)s, of volumes. '
            'E.g.: `--max-volumes 2` will download at most 2 volumes. '
            'If %(metavar)s is `0` (zero) then it will download all available volumes.'
        )
    )

    args.add_argument(
        '-a',
        '--user-agent',
        type=str,
        help=(
            'Set an user-agent. '
            'Don\'t work from protected sites.'
        )
    )

    args.add_argument(
        '-x',
        '--proxy',
        type=str,
        help=(
            'Set a http proxy.'
        )
    )

    args.add_argument(
        '-e',
        '--reverse-downloading',
        action='store_true',
        help=(
            'Download manga volumes in a reverse order. '
            'By default, manga is downloaded in ascendent order '
            '(i.e. volume 00, volume 01, volume 02...). '
            'If `--reverse-downloading` is actived, then manga is downloaded in descendent order '
            '(i.e. volume 99, volume 98, volume 97...).'
        )
    )

    args.add_argument(
        '-w',
        '--rewrite-exists-archives',
        action='store_true',
        help=(
            '(Re)Download manga volume if it already exists locally in the directory destination. '
            'Your manga files can be overwrited, so be careful.'
        )
    )

    args.add_argument(
        '-t',
        '--max-threads',
        type=int,
        default=None,
        help=(
            'Set the maximum number of threads, i.e. MAX_THREADS, to be avaliable to manga-py. '
            'Threads run in pseudo-parallel when execute the process to download the manga images.'
        )
    )

    args.add_argument(
        '-f',
        '--zero-fill',
        action='store_true',
        help=(
            'Pad a `-0` (dash-and-zero) at right for all downloaded manga volume filenames. '
            'E.g. from `vol_001.zip` to `vol_001-0.zip`. '
            'It is useful to standardize the filenames between: '
            '1) normal manga volumes (e.g. vol_006.zip) and, '
            '2) abnormal manga volumes (e.g. vol_006-5.zip). '
            'An abnormal manga volume is a released volume like: '
            'extra chapters, '
            'bonuses, '
            'updated, '
            'typos corrected, '
            'spelling errors corrected; '
            'and so on.'
        )
    )

    args.add_argument(
        '-g',
        '--with-manga-name',
        action='store_true',
        help=(
            'Pad the manga name at left for all downloaded manga volumes filenames. '
            'E.g. from `vol_001.zip` to `manga_name-vol_001.zip`.'
        )
    )

    args.add_argument(
        '-o',
        '--override-archive-name',
        metavar='ARCHIVE_NAME',
        type=str,
        default='',
        dest='override_archive_name',
        help=(
            'Pad %(metavar)s at left for all downloaded manga volumes filename. '
            'E.g from `vol_001.zip` to `%(metavar)s-vol_001.zip`.'
        )
    )

    args.add_argument(
        '-c',
        '--min-free-space',
        metavar='MB',
        type=int,
        default=100,
        help=(
            'Alert when the minimum free disc space, i.e. MB, is reached. '
            'Insert it in order of megabytes (Mb).'
        )
    )


def _reader_args(args_parser):  # pragma: no cover
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
        '-r',
        '--rename-pages',
        action='store_true',
        help=(
            'Normalize image filenames. '
            'E.g. from `0_page_1.jpg` to `0001.jpg`.'
        )
    )


def get_cli_arguments() -> ArgumentParser:  # pragma: no cover
    '''
    Method to generate manga-py CLI with its options.
    '''
    args_parser = ArgumentParser(
        add_help=False,
        formatter_class=DescriptionDefaultsHelpFormatter,
        prog="manga-py",
        description=(
            '%(prog)s is the universal manga downloader (for your offline reading).\n  '
            'Site: https://manga-py.com/manga-py/\n  '
            'Source-code: https://github.com/manga-py/manga-py\n  '
            'Version: ' + __version__
        ),
        epilog=(
            'So, that is how %(prog)s can be executed to download yours favourite mangas.\n'
            'Enjoy! 😉'
        )
    )

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
        version=__version__,
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

    _image_args(args_parser)
    _reader_args(args_parser)
    _downloading_args(args_parser)
    _debug_args(args_parser)

    return args_parser
