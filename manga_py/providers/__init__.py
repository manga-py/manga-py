from ..cli.args.args_helper import ArgsListHelper
from ..exceptions import ProviderNotFoundException
from ..libs.log import logger
from ..libs.provider import Provider
from ..providers.__list import providers


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

__all__ = ['get_provider']
