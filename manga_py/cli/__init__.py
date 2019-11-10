from manga_py.meta import version, repo_url, docs_url
from ._degug_options import _debug_options
from ._download_options import _downloading_options
from ._general_options import _general_options
from ._images_options import _images_options
from ._reader_options import _reader_options

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter


class DescriptionDefaultsHelpFormatter(ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter):
    pass


def get_options() -> ArgumentParser:
    args_parser = ArgumentParser(
        add_help=False, formatter_class=DescriptionDefaultsHelpFormatter, prog="manga-py",
        description="%(prog)s is the universal manga downloader (for your offline reading).\n "
                    " Site: {docs_url}\n"
                    " Source-code: {repo_url}\n"
                    " Version: {version}".format(version=version, repo_url=repo_url, docs_url=docs_url)
    )
    _general_options(args_parser)
    _debug_options(args_parser)
    _downloading_options(args_parser)
    _images_options(args_parser)
    _reader_options(args_parser)

    return args_parser

