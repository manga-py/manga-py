from manga_py.providers import get_provider, __merge_namespaces as merge_namespaces, manga_providers
from manga_py.provider import Provider
from manga_py.libs.base.chapter import Chapter
from manga_py.libs.base.file import File


class Api(object):
    @classmethod
    def get_provider(cls, url: str, user_providers: dict = None, user_namespaces: list = None) -> Provider:
        return get_provider(url, user_providers, user_namespaces)

    @staticmethod
    def _clean(providers):
        _list = {}
        for i in providers:
            _ = i.find('/')
            if not ~_:
                _ = i.strip('()')
            else:
                _ = i[:_].strip('()')
            _list['http://' + _.replace(r'\.', '.')] = ''
        return list(_list.keys())

    @classmethod
    def get_providers(cls, user_providers: dict = None, user_namespaces: list = None) -> list:
        """
        see get_provider.__doc__

        :param user_providers:
        :param user_namespaces:
        :return:
        :rtype list
        """
        merge_namespaces(user_providers, user_namespaces)
        providers = cls._clean(manga_providers)
        return providers

    @classmethod
    def download_chapter(cls, provider: Provider, chapter: Chapter):
        provider._store['chapter_idx'] = 0
        provider.chapter = chapter
        provider.loop_files()
