from manga_py.cli.args.args_helper import ArgsListHelper
from manga_py.exceptions import ProviderNotFoundException
from manga_py.libs.log import logger
from manga_py.libs.provider import Provider
from .__list import providers
from typing import Generator


def get_provider(url, args: ArgsListHelper) -> Generator:
    caught = False
    for _ in providers:  # type: Provider
        provider = _.new(args, url)
        if provider.supported_urls() is None:
            logger().warning(
                'SUPPORTED_URLS is None for provider %s.%s',
                provider.__class__.__module__, provider.__class__.__name__
            )
            continue
        if provider.match():
            caught = True
            yield provider

    if not caught:
        raise ProviderNotFoundException.create(url)


__all__ = ['get_provider']
