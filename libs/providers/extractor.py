import re
from libs.http import Http
from libs.image import Image


class Extractor(object):

    _params = {}
    _image_params={
        'crop': False,
        # 'crop': (0, 0, 0, 0)
        'auto_crop': False,
        # 'auto_crop': {'factor': 150, 'maximum': 40},
    }

    def __init__(self):
        self.http = Http

    def _image_params_parser(self):
        pass

    def process(self, url, path_destination, temp_dir, image_params=None, skip=0):  # Main method. Required
        pass

    # mutated methods /

    def quest(self, variants, title=''):
        pass

    def loop_file(self):
        pass

    def loop_volume(self):
        pass

    def loop_(self):
        pass

    # / mutated methods

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
