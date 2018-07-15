from argparse import ArgumentParser


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('Downloading options')

    args.add_argument('-E', '--not-change-files-extension', action='store_const',
                      help='Save files "as is"', const=True, default=False)
    args.add_argument('-u', '--update-all', action='store_const',
                      help='Update all.', const=True, default=False)
    args.add_argument('-s', '--skip-volumes', metavar='count', type=int,
                      help='Skip volumes', default=0)
    args.add_argument('-c', '--max-volumes', metavar='count', type=int,
                      help='Maximum volumes for downloading 0=All', default=0)
    args.add_argument('--user-agent', type=str, help='Don\'t work from protected sites')
    args.add_argument('--proxy', type=str, help='Http proxy')
    args.add_argument('-r', '--reverse-downloading', action='store_const',
                      help='Reverse volumes downloading', const=True, default=False)
    args.add_argument('-R', '--rewrite-exists-archives', action='store_const', const=True,
                      default=False)
    args.add_argument('-N', '--no-multi-threads', action='store_const',
                      help='Disallow multi-threads images downloading', const=True, default=False)
    args.add_argument('-z', '--zero-fill', action='store_const', const=True, default=False,
                      help='Adds 0 to the end for all chapters (vol_001.zip -> vol_001-0.zip)')
    args.add_argument('--min-free-space', metavar='Mb', type=int, default=100,
                      help='Minimum free disc space')
    args.add_argument('-w', '--with-website-name', action='store_const', const=True, default=False,
                      help='Add website name to manga name (example.org-manga_name)')
