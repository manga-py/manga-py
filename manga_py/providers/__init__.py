from manga_py.cli.args import ArgsListHelper
from manga_py.exceptions import ProviderNotFoundException
from manga_py.libs.log import logger
from manga_py.libs.provider import Provider
from manga_py.providers.__list import providers


def get_provider(url, args: ArgsListHelper) -> Provider:
    caught = False
    for _ in providers:  # type: Provider
        provider = _.new(args, url)
        if provider.SUPPORTED_URLS is None:
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
