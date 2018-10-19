from argparse import ArgumentParser

from manga_py.meta import __version__


def _image_args(args_parser):  # pragma: no cover
    args = args_parser.add_argument_group('Image options')

    args.add_argument('--not-change-files-extension', action='store_const',
                      help='Save files to archive "as is"', const=True, default=False)

    # args.add_argument('--force-png', action='store_const',
    #                          help='Force conversation images to png format', const=True, default=False)
    # args.add_argument('--force-jpg', action='store_const',
    #                          help='Force conversation images to jpg format', const=True, default=False)
    args.add_argument('--no-webp', action='store_const', const=True, default=False,
                             help='Force conversation webp images to jpg format')

    # args.add_argument('-xt', type=int, help='Manual image crop with top side', default=0)
    # args.add_argument('-xr', type=int, help='Manual image crop with right side', default=0)
    # args.add_argument('-xb', type=int, help='Manual image crop with bottom side', default=0)
    # args.add_argument('-xl', type=int, help='Manual image crop with left side', default=0)
    # args.add_argument('--crop-blank', action='store_const', help='Crop white lines on image',
    #                          const=True, default=False)


def _debug_args(args_parser):  # pragma: no cover
    args = args_parser.add_argument_group('Debug / Simulation options')

    args.add_argument('-h', '--help', action='help', help='show help and exit')
    args.add_argument('--print-json', action='store_const', const=True, default=False,
                      help='Print information about the results in the form of json (after completion)')

    args.add_argument('--simulate', action='store_const', const=True, default=False,
                      help='Do not download the files and do not write anything to disk')

    # args.add_argument('--full-error', action='store_const', const=True, default=False,
    #                   help='Show full stack trace')

    # args.add_argument('-vv', '--log', metavar='info', type='str', help='Verbose log')


def _downloading_args(args_parser):  # pragma: no cover
    args = args_parser.add_argument_group('Downloading options')

    # args.add_argument('-U', '--update-all', action='store_const',
    #                   help='Update all. Not worked now!', const=True, default=False)
    args.add_argument('-s', '--skip-volumes', metavar='count', type=int,
                      help='Skip volumes', default=0)
    args.add_argument('-c', '--max-volumes', metavar='count', type=int,
                      help='Maximum volumes for downloading 0=All', default=0)
    args.add_argument('--user-agent', type=str, help='Don\'t work from protected sites')
    args.add_argument('--proxy', type=str, help='Http proxy')
    args.add_argument('--reverse-downloading', action='store_const',
                      help='Reverse volumes downloading', const=True, default=False)
    args.add_argument('--rewrite-exists-archives', action='store_const', const=True,
                      default=False)
    args.add_argument('-nm', '--no-multi-threads', action='store_const',
                      help='Disallow multi-threads images downloading', const=True, default=False)
    args.add_argument('--one-thread', action='store_const',
                      help='Disallow multi-threads images downloading', const=True, default=False)
    args.add_argument('--zero-fill', action='store_const', const=True, default=False,
                      help='Adds 0 to the end for all chapters (vol_001.zip -> vol_001-0.zip)')
    args.add_argument('-N', '--with-manga-name', action='store_const', const=True, default=False,
                      help='Adds 0 to the end for all chapters (vol_001.zip -> manga_name-vol_001.zip)')
    args.add_argument('--min-free-space', metavar='Mb', type=int,
                      help='Minimum free disc space', default=100)


def _reader_args(args_parser):  # pragma: no cover
    args = args_parser.add_argument_group('Archive options')

    args.add_argument('--cbz', action='store_const', default=False,
                      const=True, help='Make *.cbz archives (for reader)')

    args.add_argument('--rename-pages', action='store_const', default=False, const=True,
                      help='Normalize images names. (example: 0_page_1.jpg -> 0001.jpg)')


def get_cli_arguments() -> ArgumentParser:  # pragma: no cover
    args_parser = ArgumentParser(add_help=False)
    args = args_parser.add_argument_group('General options')

    args.add_argument('url', metavar='url', type=str, help='Downloaded url')
    args.add_argument('--version', action='version', version=__version__)

    args.add_argument('-n', '--name', metavar='name', type=str, help='Manga name', default='')
    args.add_argument('-d', '--destination', metavar='path', type=str,
                      help='Destination folder (Default = current directory', default='Manga')
    args.add_argument('-np', '--no-progress', metavar='no-progress', action='store_const',
                      const=True, help='Don\'t show progress bar', default=False)
    # future
    # args_parser.add_argument('--server', action='store_const', const=True, help='Run web interface',
    #                          default=False)

    _image_args(args_parser)
    _reader_args(args_parser)
    _downloading_args(args_parser)
    _debug_args(args_parser)

    return args_parser
