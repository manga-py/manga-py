import re
from manga_py.provider import Provider
from .__list import providers_list


def __check_provider(reg, provider, url, fromlist: list):
    if re.search(reg, url):
        for _from in fromlist:
            try:
                return __import__('{}.{}'.format(_from, provider), fromlist=[_from])
            except ImportError:
                pass
    return None


def __merge_namespaces(providers, namespaces):
    if namespaces is None:
        namespaces = []
    if providers is None:
        providers = {}
    providers_list.update(providers)
    namespaces.append('manga_py.libs.providers')
    return namespaces


def _boundary(items):
    result = []
    for i in items:
        if i.find(r'\b') == -1:
            i = r'\b' + i
        result.append(i)
    return result


def get_provider(url: str, providers: dict = None, more_namespaces: list = None):
    """
    Allows you to add your namespaces to search for providers.

    Your class must be inherited from manga_py.provider.Provider and the provider must have the `main` attribute
    See example provider

    To do this, you need to register your namespace and pass it to the function get_provider()
    Your classes must be inherited from manga_py.provider.Provider
    Priority remains for the transferred namespaces

    Example:
    url = 'http://example.org/manga/path/here'
    providers = {
        'manga_provider1': [r'example1\.org/manga/.', r'example1\.org/chapter/.',]
        'manga_provider2': [r'example2\.org/manga/.', r'example2\.org/chapter/.',]
    }
    namespaces = ['my_namespace1.providers', 'my_namespace2.providers_list']

    provider = get_provider (url, providers, namespaces)

    :param url: str
    :type url str
    :param providers:
    :type providers dict
    :param more_namespaces:
    :type more_namespaces list
    :return:
    :rtype: Provider
    """
    namespaces = __merge_namespaces(providers, more_namespaces)
    for provider in providers_list:
        items = providers_list[provider]
        reg = '(?:' + '|'.join(_boundary(items)) + ')'
        provider = __check_provider(reg, provider, url, namespaces)
        if isinstance(provider, Provider) and hasattr(provider, 'main'):
            return provider.main
    raise ImportError('Provider not found')
