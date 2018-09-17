import re
from os import path
from sys import stderr

from lxml.html import HtmlElement

from manga_py.http import Http
from manga_py.image import Image


class Base:
    _storage = None
    _params = None
    _image_params = None
    _http_kwargs = None
    __http = None

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
        try:
            if not self._storage.get('domain_uri', None):
                self._storage['domain_uri'] = re.search('(https?://[^/]+)', self._params['url']).group(1)
            return self._storage.get('domain_uri', '')
        except Exception:
            print('url is broken!', file=stderr)
            exit()

    @staticmethod
    def image_auto_crop(src_path, dest_path=None):
        image = Image(src_path=src_path)
        image.crop_auto(dest_path=dest_path)
        image.close()

    def image_manual_crop(self, src_path, dest_path=None):  # sizes: (left, top, right, bottom)
        if isinstance(self._image_params['crop'], tuple) != (0, 0, 0, 0):
            image = Image(src_path=src_path)
            image.crop_manual_with_offsets(offsets=self._image_params['crop'], dest_path=dest_path)
            image.close()

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
        if self._params.get('cf_protect', False):
            return ua_storage
        return ua_params

    @property
    def chapter_id(self):
        return self._storage.get('current_chapter', 0)

    @chapter_id.setter
    def chapter_id(self, idx):
        self._storage['current_chapter'] = idx

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
