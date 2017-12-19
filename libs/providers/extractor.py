import re
from libs import fs
from libs.http import Http
from libs.image import Image


class Extractor(object):

    _params = {
    }
    _image_params = {
        'crop': False,
        # 'crop': (0, 0, 0, 0)
        'auto_crop': False,
        # 'auto_crop': {'factor': 150, 'maximum': 40},
    }
    _volumes_count = 0

    def __init__(self):
        self.http = Http
        self._params['temp_directory'] = fs.get_temp_path()

    # mutated methods /

    def get_main_content(self):  # call once
        pass

    def get_volumes(self):  # call once
        pass

    def get_cookies(self):  # if site with cookie protect
        pass

    def get_files(self):  # call ever volume loop
        pass

    def quest(self, variants, title=''):  # return callback ?
        pass

    def loop_volume(self):  # call ever volume
        pass

    def loop_file(self):  # call ever file. After downloading
        pass

    # / mutated methods

    def process(self, url, downloading_params=None, image_params=None):  # Main method
        self._params['url'] = url
        self._downloading_params_parser(downloading_params)
        self._image_params_parser(image_params)

    def _image_params_parser(self, params):
        self._set_if_not_none(self._image_params, 'crop', params.get('crop', None))
        self._set_if_not_none(self._image_params, 'auto_crop', params.get('auto_crop', None))

    @staticmethod
    def _set_if_not_none(var, key, value):
        if value is not None:
            var[key] = value

    def _downloading_params_parser(self, params):
        self._set_if_not_none(self._params, 'path_destination', params.get('path_destination', None))

    def re_match(self, pattern, string, flags=0):
        return re.match(pattern, string, flags)

    def re_search(self, pattern, string, flags=0):
        return re.search(pattern, string, flags)

    def re(self) -> re:
        return re

    def downloader(self) -> callable:
        return self.http

    def image_auto_crop(self, path_src, path_dst=None):
        if not path_dst:
            path_dst = path_src
        pass

    def image_manual_crop(self, path_src, sizes=(), path_dst=None):  # sizes: (left, top, right, bottom)
        if not path_dst:
            path_dst = path_src
        pass
