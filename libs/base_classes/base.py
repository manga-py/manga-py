import re
from typing import Callable

from libs.http import Http
from libs.image import Image


class Base:
    _storage = None
    _params = None
    _image_params = None
    _http_kwargs = None

    def __init__(self):

        self._storage = {
            'cookies': {},
            'main_content': '',
            'chapters': [],
            'current_chapter': 0,
            'current_file': 0
        }
        self._params = {
            'path_destination': 'Manga'
        }
        self._image_params = {
            'crop': None,
            # 'crop': (left, upper, width, height)
            'offsets_crop': None,
            # 'crop': (left, upper, right, lower)
            'auto_crop': None,
            # 'auto_crop': {'max_crop_size': 40, 'auto_crop_factor': 150},
        }
        self._http_kwargs = {}

    def get_url(self):
        return self._params['url']

    def get_domain(self):
        domain_uri = self._storage.get('domain_uri', None)
        if not domain_uri:
            self._storage['domain_uri'] = re.search('(https?://[^/]+)', self._params['url']).group(1)

        return self._storage['domain_uri']

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

    def http(self) -> Http:
        http_params = {
            'allow_webp': not self._params.get('disallow_webp', None),
            'referer': self._storage.get('referer', self.get_domain()),
            'user_agent': self._get_user_agent(),
            'proxies': None,  # todo
            'cookies': self._storage.get('cookies', None),
            'kwargs': self._http_kwargs
        }
        http = Http(**http_params)
        return http

    def http_get(self, url: str, headers: dict = None, cookies: dict = None):
        return self.http().get(url=url, headers=headers, cookies=cookies)

    def http_post(self, url: str, headers: dict = None, cookies: dict = None, data=()):
        return self.http().post(url=url, headers=headers, cookies=cookies, data=data)

    def _call_files_progress_callback(self):
        if callable(self.files_progress_callback):
            _max, _current = len(self._storage['files']), self._storage['current_file']
            self.files_progress_callback(_max, _current, _current < 1)

    def _get_user_agent(self):
        ua_storage = self._storage.get('user_agent', None)
        ua_params = self._params.get('user_agent', None)
        if self._params.get('cf-protect', False):
            return ua_storage
        return ua_params
