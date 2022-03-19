from logging import warning
from os import path
from typing import Optional, List, Union
from requests import Response
import re

from lxml.html import HtmlElement

from manga_py.http import Http
from manga_py.http.flare_solver import Http as FS_Http
from .params import ProviderParams


CF_PROXY_RE = re.compile(r'(https?://[^/]+)')


class Base(ProviderParams):
    _storage = None
    _params = None
    _image_params = None
    _http_kwargs = None
    __http = None
    __arguments = None
    _use_flare_solver = False
    __flare_solver_http = None
    _flare_solver_url = None
    chapter_id = 0
    quiet = False
    original_url = None

    def __init__(self):

        self._storage = {
            'cookies': {},
            'main_content': None,
            'chapters': [],
            'current_chapter': 0,
            'proxies': {},
            'domain_uri': None,
        }
        self._params = {
            'destination': 'Manga',
            'cf-protect': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
        }
        self._image_params = {
            'crop': (0, 0, 0, 0),
            # 'crop': (left, upper, right, lower)
            'auto_crop': False,
            # 'auto_crop': True,
        }
        self._http_kwargs = {}

    def _archive_type(self) -> str:
        arc_type = 'zip'
        if self._params['cbz']:
            arc_type = 'cbz'
        return arc_type

    def get_url(self):
        return self._params['url']

    def _build_http_params(self, params):
        if params is None:
            params = {}
        params.setdefault('allow_webp', not self._params.get('no_webp', False))
        params.setdefault('referer', self._storage.get('referer', self.domain))
        params.setdefault('user_agent', self._get_user_agent())
        params.setdefault('proxies', self._storage.get('proxies', None))
        params.setdefault('cookies', self._storage.get('cookies', None))
        params.setdefault('kwargs', self._http_kwargs)
        return params

    def http(self, new=False, params=None) -> Union[FS_Http, Http]:
        if self._use_flare_solver:
            return self.flare_solver_http(new, params)
        else:
            return self.http_normal(new, params)

    def flare_solver_http(self, new=False, params=None) -> FS_Http:
        allow_webp = True == (params or {}).get('no_webp', False)
        headers = {}
        if allow_webp:
            headers['Accept'] = Http.webp_header
        if self.__flare_solver_http is not None:
            self.__flare_solver_http = FS_Http(self._flare_solver_url, self._get_user_agent())
            self.__flare_solver_http.create_session()
        if new:
            http = FS_Http(self._flare_solver_url, self._get_user_agent())
            http.create_session()
            return http
        return self.__flare_solver_http

    def http_normal(self, new=False, params=None) -> Http:
        http_params = self._build_http_params(params)
        if new:
            http = Http(**http_params)
            return http

        if self.__http is None:
            self.__http = Http(**http_params)

        return self.__http

    def http_get(self, url: str, headers: dict = None, cookies: dict = None):
        http = self.http()
        with http.get(url=url, headers=headers, cookies=cookies) as resp:
            if type(http) == Http:
                return resp.text
            else:
                return resp.json().get('solution', {}).get('response', b'').decode()

    def http_post(self, url: str, headers: dict = None, cookies: dict = None, data=()):
        http = self.http()
        with http.post(url=url, headers=headers, cookies=cookies, data=data) as resp:
            if type(http) == Http:
                return resp.text
            else:
                return resp.json().get('solution', {}).get('response', b'').decode()

    def _get_user_agent(self):
        return self._params.get('user_agent', None)

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

    def book_meta(self) -> dict:
        return {}

    def _image_name(self, idx, filename):
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

    def allow_auto_change_url(self):
        return True

    def cookies(self, response: Response) -> dict:
        if self._use_flare_solver:
            return response.json().get('solution', {}).get('cookies')
        return response.cookies.__dict__

    @property
    def cf_proxy(self) -> Optional[str]:
        cf = self._params.get('cf_proxy')
        if cf is not None:
            cf = CF_PROXY_RE.search(cf)
        return cf.group(1) if cf else None

    def __del__(self):
        if self.__flare_solver_http is not None:
            self.flare_solver_http().destroy_session()
