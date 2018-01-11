import re
from typing import Callable

from lxml.html import document_fromstring

from libs.fs import (
    get_temp_path,
    basename,
    remove_file_query_params,
)
from libs.http import Http, MultiThreads
from libs.image import Image


class BaseProvider:
    _storage = {
        'cookies': (),
        'main_content': '',
        'chapters': [],
        'current_chapter': 0,
        'current_file': 0
    }
    _params = {
        'path_destination': 'Manga'
    }
    _image_params = {
        'crop': None,
        # 'crop': (left, upper, width, height)
        'offsets_crop': None,
        # 'crop': (left, upper, right, lower)
        'auto_crop': None,
        # 'auto_crop': {'max_crop_size': 40, 'auto_crop_factor': 150},
    }

    @staticmethod
    def document_fromstring(body, selector: str = None, idx: int = None):
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

    @staticmethod
    def re_match(pattern, string, flags=0):
        return re.match(pattern, string, flags)

    @staticmethod
    def re_search(pattern, string, flags=0):
        return re.search(pattern, string, flags)

    @staticmethod
    def basename(_path) -> str:
        return basename(_path)

    def get_url(self):
        return self._params['url']

    def get_domain(self):
        domain_uri = self._params.get('domain_uri', None)
        if not domain_uri:
            self._params['domain_uri'] = re.search('(https?://[^/]+)', self._params['url']).group(1)

        return self._params['domain_uri']

    def get_current_chapter(self):
        return self._storage['chapters'][self._storage['current_chapter']]

    def get_current_file(self):
        return self._storage['files'][self._storage['current_file']]

    def quest_callback(self, variants: enumerate, title: str, select_type=0):  # 0 = single, 1 = multiple
        pass

    def files_progress_callback(self, max_val: int, current_val: int, need_reset=False):
        pass

    def logger_callback(self, *args):
        pass

    def set_quest_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'quest_callback', callback)

    def set_progress_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'files_progress_callback', callback)

    def set_logger_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'logger_callback', callback)

    def get_referrer(self):
        return self.referrer if hasattr(self, 'referrer') else self.get_domain()

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

    def _site_cookies(self) -> list:
        if not isinstance(self._storage['cookies'], list):
            return []
        return [i for i in self._storage['cookies'] if isinstance(i, dict)]

    def http(self) -> Http:
        http_params = {
            'allow_webp': not self._params.get('disallow_webp', None),
            'referrer_url': self.get_referrer(),
            'user_agent': self._params.get('user_agent', None),
            'proxies': None,  # todo
            'cookies': self._site_cookies(),
        }
        http = Http(**http_params)
        return http

    def http_get(self, url: str, headers: dict = None, cookies: dict = None):
        return self.http().get(url=url, headers=headers, cookies=cookies)

    def http_post(self, url: str, headers: dict = None, cookies: dict = None):
        return self.http().post(url=url, headers=headers, cookies=cookies)

    def _call_files_progress_callback(self):
        if self.files_progress_callback:
            _max, _current = len(self._storage['files']), self._storage['current_file']
            self.files_progress_callback(_max, _current, _current < 1)
