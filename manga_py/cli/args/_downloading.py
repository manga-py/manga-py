from argparse import ArgumentParser


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('Downloading options')

    args.add_argument('-E', '--not-change-files-extension', action='store_true', help='Save files "as is"')
    args.add_argument('-U', '--update-all', action='store_true', help='Update all.')
    args.add_argument('-s', '--skip-volumes', metavar='count', type=int, default=0,
                      help='Skip volumes (Works on one only url!)')
    args.add_argument('-c', '--max-volumes', metavar='count', type=int,
                      help='Maximum volumes for downloading 0=All (Works on one only url!)', default=0)
    args.add_argument('-u', '--user-agent', type=str,
                      help='Don\'t work from protected sites, don\'t work on update mode!')
    args.add_argument('--proxy', type=str, help='Http proxy')
    args.add_argument('-r', '--reverse-downloading', action='store_true', help='Reverse volumes downloading')
    args.add_argument('-R', '--rewrite-exists-files', action='store_true', help='(Don\'t work on update mode!)')
    args.add_argument('-T', '--no-multi-threads', action='store_true', help='Disallow multi-threads images downloading')
    args.add_argument('-z', '--zero-fill', action='store_true',
                      help='Adds 0 to the end for all chapters (vol_001.zip -> vol_001-0.zip)')
    args.add_argument('--min-free-space', metavar='Mb', type=int, default=200,
                      help='Minimum free disc space in Mb (default=200)')
    args.add_argument('-N', '--with-website-name', action='store_true',
                      help='Add website name to manga name (example.org-manga_name)')
