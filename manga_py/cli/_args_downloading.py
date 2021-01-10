
def _args_downloading(args_parser):  # pragma: no cover
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
        '-c',
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
        '-u',
        '--user-agent',
        type=str,
        help=(
            'Set an user-agent. '
            # 'Don\'t work from protected sites.'
        )
    )

    args.add_argument(
        '--cookies',
        type=str,
        help=(
            'Set specified cookies. Example: --cookies cf_clearance=9c.. test=5a..'
        ),
        nargs='*',
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
        '-r',
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
        default=4,
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
        '-p',
        '--force-provider',
        metavar='URL',
        type=str,
        help='Force use specific provider',
    )

    args.add_argument(
        '-N',
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
        '-S',
        '--min-free-space',
        metavar='MB',
        type=int,
        default=100,
        help=(
            'Alert when the minimum free disc space, i.e. MB, is reached. '
            'Insert it in order of megabytes (Mb).'
        )
    )

    args.add_argument(
        '--skip-incomplete-chapters',
        action='store_true',
        help=(
            'Incomplete chapters are not written to disk instead of saving them as "IMAGES_SKIP_ERROR"'
        )
    )

