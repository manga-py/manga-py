import re

from manga_py.cli.args import ArgsListHelper
from manga_py.exceptions import ProviderNotFoundException
from manga_py.libs.provider import Provider
from manga_py.providers.__list import providers


def get_provider(url, args: ArgsListHelper) -> Provider:
    caught = False
    for provider in providers:  # type: Provider
        supported = False
        if provider.SUPPORTED_URLS is None:
            continue
        for i in provider.SUPPORTED_URLS:
            if re.search(i, url):
                supported = True
                caught = True
                break
        if supported:
            yield provider.new(args, url)

    if not caught:
        raise ProviderNotFoundException.create(url)
