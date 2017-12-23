import re
import json
from abc import abstractmethod
from os.path import basename
from lxml.html import document_fromstring
from libs.fs import get_temp_path
from libs.http import Http
from libs.image import Image


class Provider:

    _params = {
    }
    _image_params = {
        'crop': False,
        # 'crop': (left, upper, width, height)
        'offsets_crop': False,
        # 'crop': (left, upper, right, lower)
        'auto_crop': False,
        # 'auto_crop': {'max_crop_size': 40, 'auto_crop_factor': 150},
    }
    _volumes_count = 0
    _storage = {
        'cookies': (),
        'main_content': '',
        'chapters': [],
        'current_chapter': 0,
        'current_file': 0
    }
    files_progress_callback = None

    def __init__(self):
        self.re = re
        self.json = json
        self.http = Http
        self._params['temp_directory'] = get_temp_path()

    def _image_params_parser(self, params):
        params = params if isinstance(params, dict) else {}
        self._set_if_not_none(self._image_params, 'crop', params.get('crop', None))
        self._set_if_not_none(self._image_params, 'auto_crop', params.get('auto_crop', None))

    def _downloading_params_parser(self, params):
        params = params if isinstance(params, dict) else {}
        self._set_if_not_none(self._params, 'path_destination', params.get('path_destination', None))
        self._set_if_not_none(self._params, 'path_destination', params.get('path_destination', None))

    def process(self, url, downloading_params=None, image_params=None):  # Main method
        self._params['url'] = url
        self._downloading_params_parser(downloading_params)
        self._image_params_parser(image_params)

        self._storage['cookies'] = self.get_cookies()
        self._storage['main_content'] = self.get_main_content()
        self._storage['chapters'] = self.get_chapters()

        self.loop_volumes()

    # mutated methods /

    def get_main_content(self):  # call once
        return self.http_get(self.get_url())

    @abstractmethod
    def get_manga_name(self) -> str:  # call once
        return ''

    @abstractmethod
    def get_chapters(self) -> list:  # call once
        return []

    @abstractmethod
    def get_cookies(self):  # if site with cookie protect
        pass

    @abstractmethod
    def get_files(self) -> list:  # call ever volume loop
        return []

    @abstractmethod
    def _loop_callback_volumes(self):
        pass

    @abstractmethod
    def _loop_callback_files(self):
        pass
    
    def get_archive_name(self):
        return basename(self.get_current_file())

    # / mutated methods

    def quest(self, variants: enumerate, title: str, select_type=0):  # 0 = single, 1 = multiple
        pass

    def set_quest_callback(self, callback: callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'quest', callback)

    def __call_files_progress_callback(self):
        if self.files_progress_callback:
            _max, _current = len(self._storage['files']), len(self._storage['current_file'])
            self.files_progress_callback(_max, _current, _current < 1)

    def loop_volumes(self):
        volumes = self._storage['chapters']
        if isinstance(volumes, list) and len(volumes) > 0:
            for idx in volumes:
                self._storage['current_chapter'] = idx
                self._loop_callback_volumes()
                self._storage['files'] = self.get_files()
                self.loop_files()

    def loop_files(self):
        files = self._storage['files']
        if isinstance(files, list) and len(files) > 0:
            for idx in files:
                self._storage['current_file'] = idx
                self.__call_files_progress_callback()
                self._loop_callback_files()
                self.save_file()

    def html_fromstring(self, addr, selector: str = None, idx: int = None):
        return self.document_fromstring(self.http_get(addr), selector, idx)

    def document_fromstring(self, body, selector: str = None, idx: int = None):
        result = document_fromstring(body)
        if isinstance(selector, str):
            result = result.cssselect(selector)
        if isinstance(idx, int):
            result = result[abs(idx)]
        return result

    @staticmethod
    def _set_if_not_none(var, key, value):
        if value is not None:
            var[key] = value

    def re_match(self, pattern, string, flags=0):
        return re.match(pattern, string, flags)

    def re_search(self, pattern, string, flags=0):
        return re.search(pattern, string, flags)

    def http(self) -> Http:
        http_params = {
            'allow_webp': None,
            'referrer_url': None,
            'user_agent': self._params.get('user_agent', None),
            'proxies': None,
            'site_cookies': None,
        }
        http = self.http(**http_params)
        return http

    def http_get(self, url: str, headers: dict = None, cookies: dict = None):
        return self.http().get(url=url, headers=headers, cookies=cookies)

    def http_post(self, url: str, headers: dict = None, cookies: dict = None):
        return self.http().post(url=url, headers=headers, cookies=cookies)

    def image_auto_crop(self, src_path, dest_path=None):
        image = Image(src_path=src_path)
        if isinstance(self._image_params['auto_crop'], dict):
            for i in self._image_params['auto_crop']:
                image.params[i] = self._image_params['auto_crop'][i]
        image.crop_auto(dest_path=dest_path)

    def image_manual_crop(self, src_path, dest_path=None):  # sizes: (left, top, right, bottom)
        if isinstance(self._image_params['crop'], tuple):
            image = Image(src_path=src_path)
            image.crop_manual(sizes=self._image_params['crop'], dest_path=dest_path)
        elif isinstance(self._image_params['offsets_crop'], tuple):
            image = Image(src_path=src_path)
            image.crop_manual_with_offsets(offsets=self._image_params['offsets_crop'], dest_path=dest_path)

    def get_url(self):
        return self._storage['url']

    def get_domain_uri(self):
        domain_uri = self._params.get('domain_uri', None)
        if not domain_uri:
            self._params['domain_uri'] = re.search('(https?://[^/]+)', self._params['url']).group(1)

        return self._params['domain_uri']

    def get_current_chapter(self):
        return self._storage['chapters'][self._storage['current_chapter']]

    def get_current_file(self):
        return self._storage['files'][self._storage['current_file']]

    def save_file(self):
        # TODO
        pass
