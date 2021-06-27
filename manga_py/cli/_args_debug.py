import argparse
import platform

import pkg_resources
from ..meta import version
from ._requirements import requirements

requires = []


def package_version(name: str) -> str:
    try:
        pkg = __import__(name)
        return pkg.__version__
    except ImportError:
        try:
            return pkg_resources.get_distribution(name).version
        except pkg_resources.DistributionNotFound:
            return ''


def print_versions(versions):
    length = [max(len(v[i]) for v in versions) for i in [0, 1]]

    for line in versions:
        print(f"{line[0]:{length[0]}} | {line[1]:{length[1]}}")


class DebugVersionAction(argparse.Action):
    def __init__(
            self,
            option_strings,
            dest,
            default=None,
            required=False,
            help=None,
    ):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            default=default,
            required=required,
            help=help
        )

    def print_versions_help(self):
        versions = [
            ("Component", "Version"),
            ("---", "---"),
            ("OS", platform.platform(aliased=True)),
            ("python", platform.python_version()),
            ("pip", package_version('pip')),
            ("manga-py", version),
        ]
        print_versions(versions)
        print("")
        module_versions = [
            ("Module", "Version"),
            ("---", "---"),
        ]
        module_versions.extend(
            sorted(
                [(req, package_version(req)) for req in requirements]
            )
        )
        print_versions(module_versions)

    def __call__(self, parser, namespace, values, option_string=None):
        self.print_versions_help()
        exit(0)


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
        '--debug-version',
        action=DebugVersionAction,
        help=(
            'Print debug version info.'
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
