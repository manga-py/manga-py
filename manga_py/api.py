from typing import List

from manga_py.libs.base import File
from manga_py.libs.base.chapter import Chapter
# from manga_py.libs.base.file import File
from manga_py.provider import Provider
from manga_py.providers import (
    get_provider as _get_provider,
    __merge_namespaces as _merge_namespaces,
    manga_providers as _manga_providers
)


def get_provider(url: str, user_providers: dict = None, user_namespaces: list = None) -> Provider:
    return _get_provider(url, user_providers, user_namespaces)


def _clean(providers) -> List[str]:
    _list = []
    for i in providers:
        _ = i.find('/')
        if not ~_:
            _ = i.strip('()')
        else:
            _ = i[:_].strip('()')
        _list.append('http://' + _.replace(r'\.', '.'))
    return list(set(_list))


def get_supported_resources(user_providers: dict = None, user_namespaces: list = None) -> List[str]:
    """
    :param user_providers:
    :param user_namespaces:
    :return: ['http://example.org',]
    """
    _merge_namespaces(user_providers, user_namespaces)
    return _clean(_manga_providers)


def download_chapter(provider: Provider, chapter: Chapter):
    provider._store['chapter_idx'] = 0
    provider.chapter = chapter
    provider.loop_files()


def det_chapter_files(provider: Provider, chapter: Chapter) -> List[File]:
    provider._store['chapter_idx'] = 0
    provider.chapter = chapter
    return provider.files


def det_chapters(provider: Provider) -> List[Chapter]:
    return provider.chapters
