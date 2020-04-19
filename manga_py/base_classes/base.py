from os import path
from urllib.parse import urlparse
from typing import Optional, List

from logging import warning, error
from lxml.html import HtmlElement

from manga_py.http import Http
from manga_py.manga_image import MangaImage


class Base:
    _storage = None
    _params = None
    _image_params = None
    _http_kwargs = None
    __http = None
    __quiet = False
    __arguments = None
    chapter_id = 0
    quiet = False

    def __init__(self):

        self._storage = {
            'cookies': {},
            'main_content': None,
            'chapters': [],
            'current_chapter': 0,
            'current_file': 0,
            'proxies': {},
            'domain_uri': None,
        }
        self._params = {
            'destination': 'Manga',
            'cf-protect': False,
        }
        self._image_params = {
            'crop': (0, 0, 0, 0),
            # 'crop': (left, upper, right, lower)
            'auto_crop': False,
            # 'auto_crop': True,
        }
        self._http_kwargs = {}

    def _archive_type(self):
        arc_type = 'zip'
        if self._params['cbz']:
            arc_type = 'cbz'
        return arc_type

    def get_url(self):
        return self._params['url']

    @property
    def domain(self) -> str:
        _url = self._params['url']
        try:
            if not self._storage.get('domain_uri', None):
                parsed = urlparse(_url, 'https')
                self._storage['domain_uri'] = '{}://{}'.format(
                    parsed.scheme,
                    parsed.netloc
                )
            return self._storage.get('domain_uri', '')
        except Exception:
            error('url "%s" is broken!' % _url)
            exit()

    def _build_http_params(self, params):
        if params is None:
            params = {}
        params.setdefault('allow_webp', not self._params.get('disallow_webp', None))
        params.setdefault('referer', self._storage.get('referer', self.domain))
        params.setdefault('user_agent', self._get_user_agent())
        params.setdefault('proxies', self._storage.get('proxies', None))
        params.setdefault('cookies', self._storage.get('cookies', None))
        params.setdefault('kwargs', self._http_kwargs)
        return params

    def http(self, new=False, params=None) -> Http:
        http_params = self._build_http_params(params)
        if new:
            http = Http(**http_params)
            return http
        elif not self.__http:
            self.__http = Http(**http_params)
        return self.__http

    def http_get(self, url: str, headers: dict = None, cookies: dict = None):
        return self.http().get(url=url, headers=headers, cookies=cookies)

    def http_post(self, url: str, headers: dict = None, cookies: dict = None, data=()):
        return self.http().post(url=url, headers=headers, cookies=cookies, data=data)

    def _get_user_agent(self):
        ua_storage = self._storage.get('user_agent', None)
        ua_params = self._params.get('user_agent', None)
        if self._params.get('cf_scrape', False):
            return ua_storage
        return ua_params

    @classmethod
    def __normalize_chapters(cls, n, element):
        if isinstance(element, HtmlElement):
            return n(element.get('href'))
        if isinstance(element, str):
            return n(element)
        return element

    def _prepare_chapters(self, chapters):
        n = self.http().normalize_uri
        items = []
        if chapters and len(chapters):
            for i in chapters:
                url = self.__normalize_chapters(n, i)
                items.append(url)
        else:
            warning('Chapters list empty. Check %s' % self.get_url())
        return items

    @property
    def chapter(self):
        return self._storage['chapters'][self.chapter_id]

    def get_current_file(self):
        return self._storage['files'][self._storage['current_file']]

    def book_meta(self) -> dict:
        return {}

    def _image_name(self, idx, filename):
        if idx is None:
            idx = self._storage['current_file']
        fn, extension = path.splitext(filename)
        _path = '{:0>3}_{}'.format(idx, fn)
        if self._params['rename_pages']:
            _path = '{:0>3}'.format(idx)
        return _path + extension

    def chapter_for_json(self) -> str:
        return self.chapter

    def put_info_json(self, meta):
        # manga_name, url, directory
        pass

    def _fill_arguments(self, arguments: List[str]):
        know_args = [
            'login',
            'password',
            'language',
            'translator',
        ]

        if self.__arguments is None:
            self.__arguments = {}

        for arg in arguments:
            key, value = arg.split('=', 1)  # type: str, str
            if key in know_args:
                self.__arguments[key] = value

    def arg(self, key: str) -> Optional[str]:
        if self.__arguments is None:
            return None
        return self.__arguments.get(key)

