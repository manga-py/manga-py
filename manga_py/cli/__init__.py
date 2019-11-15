from manga_py.meta import version, repo_url, docs_url
from .options import parse_options

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
    parse_options(args_parser)

    return args_parser

