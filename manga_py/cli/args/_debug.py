from argparse import ArgumentParser

from manga_py.meta import __version__


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('Debug / Simulation options')

    args.add_argument('-h', '--help', action='help', help='show help and exit')
    args.add_argument('-v', '--version', action='version', version=__version__)
    args.add_argument('-J', '--print-json', action='store_true', const=True,
                      help='Print information about the results in the form of json (after completion)')

    args.add_argument('-S', '--simulate', action='store_true', const=True,
                      help='Do not download the files and do not write anything to disk')

    args.add_argument('-l', '--show-log', action='store_true', const=True,
                      help='Print log (Don\'t show progress bar)')

    args.add_argument('-P', '--no-progress', action='store_true',
                      const=True, help='Don\'t show progress bar')

    args.add_argument('--force-make-db', action='store_true',
                      const=True, help='Don\'t show progress bar')

    args.add_argument('-D', '--do-not-use-database', action='store_true',
                      help='Run manga-py without database', const=True)

    args.add_argument('-T', '--do-not-clear-temporary-directory', action='store_false',
                      help='Don\'t clear temporary directory after exit', const=True)
