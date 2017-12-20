import re
import json
from lxml.html import document_fromstring
from libs import fs
from libs.http import Http
from libs.image import Image


class Extractor(object):

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
        'volumes': [],
        'current_volume': 0,
        'current_file': 0
    }

    def __init__(self):
        self.http = Http
        self._params['temp_directory'] = fs.get_temp_path()

    # mutated methods /

    def get_main_content(self):  # call once
        pass

    def get_manga_name(self):  # call once
        pass

    def get_volumes(self):  # call once
        pass

    def get_cookies(self):  # if site with cookie protect
        pass

    def get_files(self):  # call ever volume loop
        pass

    def _loop_callback_volumes(self):
        pass

    def _loop_callback_files(self):
        pass

    # / mutated methods

    def quest(self, variants: list, title=''):  # return callback ?
        pass

    def loop_volumes(self):
        volumes = self._storage['volumes']
        if isinstance(volumes, list) and len(volumes) > 0:
            for idx in volumes:
                self._storage['current_volume'] = idx
                self._loop_callback_volumes()
                self._storage['files'] = self.get_files()
                self.loop_files()

    def loop_files(self):
        files = self._storage['files']
        if isinstance(files, list) and len(files) > 0:
            for idx in files:
                self._storage['current_file'] = idx
                self._loop_callback_files()

    def process(self, url, downloading_params=None, image_params=None):  # Main method
        self._params['url'] = url
        self._downloading_params_parser(downloading_params)
        self._image_params_parser(image_params)

        self._storage['cookies'] = self.get_cookies()
        self._storage['main_content'] = self.get_main_content()
        self._storage['volumes'] = self.get_volumes()

        self.loop_volumes()

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

    def _image_params_parser(self, params):
        params = params if isinstance(params, dict) else {}
        self._set_if_not_none(self._image_params, 'crop', params.get('crop', None))
        self._set_if_not_none(self._image_params, 'auto_crop', params.get('auto_crop', None))

    def _downloading_params_parser(self, params):
        params = params if isinstance(params, dict) else {}
        self._set_if_not_none(self._params, 'path_destination', params.get('path_destination', None))

    def re_match(self, pattern, string, flags=0):
        return re.match(pattern, string, flags)

    def re_search(self, pattern, string, flags=0):
        return re.search(pattern, string, flags)

    def re(self) -> re:
        return re

    def json(self) -> json:
        return json

    def http(self) -> Http:
        http_params = {
            'allow_webp': None,
            'referrer_url': None,
            'user_agent': None,
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
            for i in self._image_params:
                image.params[i] = self._image_params['auto_crop'][i]
        image.crop_auto(dest_path=dest_path)

    def image_manual_crop(self, src_path, dest_path=None):  # sizes: (left, top, right, bottom)
        if isinstance(self._image_params['crop'], tuple):
            image = Image(src_path=src_path)
            image.crop_manual(sizes=self._image_params['crop'], dest_path=dest_path)
        elif isinstance(self._image_params['offsets_crop'], tuple):
            image = Image(src_path=src_path)
            image.crop_manual_with_offsets(offsets=self._image_params['offsets_crop'], dest_path=dest_path)
