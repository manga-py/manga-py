from argparse import ArgumentParser


def downloading_options(args_parser: ArgumentParser):  # pragma: no cover
    args = args_parser.add_argument_group('Downloading options')

    args.add_argument('-s', '--skip-volumes', metavar='COUNT', type=int,
                      help='Skip a total number, i.e. %(metavar)s, of volumes.', default=0)

    args.add_argument('-c', '--max-volumes', metavar='COUNT', type=int, default=0,
                      help='Download a maximum number, i.e. %(metavar)s, of volumes. '
                           'E.g.: `--max-volumes 2` will download at most 2 volumes. '
                           'If %(metavar)s is `0` (zero) then it will download all available volumes.')

    args.add_argument('--user-agent', type=str, help='Set an user-agent.')

    args.add_argument('--proxy', type=str, help='Set a http proxy.')

    args.add_argument('--reverse-downloading', action='store_true',
                      help='Download manga volumes in a reverse order.'
                           ' By default, the manga will be downloaded in a ascendent order'
                           ' (i.e. volume 00, volume 01, volume 02...).'
                           ' If `--reverse-downloading` has been actived, '
                           'then the manga will be downloaded in a descendent order '
                           '(i.e. volume 99, volume 98, volume 97...).')

    args.add_argument('--rewrite-exists-archives', action='store_true',
                      help='(Re)Download manga volume if it already exists locally in the directory destination.'
                           ' Your manga files can be overwrited, so be careful.')

    args.add_argument('-nm', '--max-threads', type=int, default=None,
                      help='Set the maximum number of threads, i.e. MAX_THREADS,'
                           ' to be ready to use when downloading the manga images.')

    args.add_argument('--zero-fill', action='store_true',
                      help='Pad a `-0` (dash-and-zero) at right for all downloaded manga volume filenames.'
                           ' E.g. from `vol_001.zip` to `vol_001-0.zip`.'
                           ' It is useful to standardize the filenames between normal manga volumes'
                           ' (e.g. vol_006.zip) and the extra/bonuses/updated/corrected manga volumes'
                           ' (e.g. vol_006-5.zip) released by scanlators groups.')

    args.add_argument('-N', '--with-manga-name', action='store_true',
                      help='Pad the manga name at left for all downloaded manga volumes filenames.'
                           ' E.g. from `vol_001.zip` to `manga_name-vol_001.zip`.')

    args.add_argument('--min-free-space', metavar='MB', type=int, default=100,
                      help='Alert when the minimum free disc space, i.e. MB, is reached.'
                           ' Insert it in order of megabytes (Mb).')


__all__ = ['downloading_options']
