from manga_py import meta
from datetime import datetime
from argparse import Namespace
from json import dumps
from sys import argv


class Info:
    __doc__ = """
    --print-json argument helper
    
    {
        'site': 'https://example.org/kumo-desu-ga-nani-ka',
        'downloader': 'https://github.com/yuru-yuri/manga-dl',
        'version': '1.1.4',
        'delta': '0:00:00.003625',
        'start': '2018-06-08 17:22:24.419565',
        'end': '2018-06-08 17:22:24.423190',
        'user_agent': 'Mozilla/5.0',
        'cookies': {'cf_clearance': 'ec-1528654923-86400', '__cfduid': '21528654914'},
        'args': {
            '_raw_params': 'manga-py --cbz https://example.org/kumo-desu-ga-nani-ka',
            'url': 'https://example.org/kumo-desu-ga-nani-ka',
            'name': None,
            'destination': None,
            'no-progress': False,
            'cbz': False,
            'skip-volumes': None,
            'max-volumes': None,
            'user-agent': None,
            'proxy': None,
            'reverse-downloading': None,
            'rewrite-exists-archives': None,
            'no-multi-threads': None,
        },
        'return_code': 0,
        'error': '',
        'volumes': [
            {
              'name': 'Kumo desu ga, nani ka? - 0',
              'path': 'Manga/kumo-desu-ga-nani-ka/vol_000.zip',
              'error': False,

              'num_pages': '8',  # Only with option --full-json-info
              'pages': [  # Only with option --full-json-info
                    '000_p_00001.jpg',  # Only with option --full-json-info
                    '001_p_00002.jpg',  # Only with option --full-json-info
                    '002_p_00003.jpg',  # Only with option --full-json-info
                    '003_p_00004.jpg',  # Only with option --full-json-info
                    '004_p_00005.jpg',  # Only with option --full-json-info
                    '005_p_00006.jpg',  # Only with option --full-json-info
                    '006_p_00007.jpg',  # Only with option --full-json-info
                    '007_p_00008.jpg',  # Only with option --full-json-info
              ],  # Only with option --full-json-info

            },
            {
              'name': 'Kumo desu ga, nani ka? - 1',
              'path': 'Manga/kumo-desu-ga-nani-ka/vol_001.zip',
              'error': False,
            },
        ],
    }
    """
    _data = None
    _init_time = None
    _start_time = None

    @staticmethod
    def _dt(dt, fmt: str = '%A, %d. %B %Y %H:%M:%S'):
        return dt.strftime(fmt)

    def __init__(self, args: Namespace):  # see manga_py.cli arguments
        self._init_time = datetime.now()
        _args = args.__dict__
        _args['_raw_params'] = ' '.join(argv)
        self._data = {
            'site': args.url,
            'downloader': meta.__downloader_uri__,
            'version': meta.__version__,
            'delta': None,
            'start': None,
            'end': None,
            'user_agent': None,
            'cookies': None,
            'args': _args,
            'return_code': None,
            'error': '',
            'volumes': [],
        }
        self._volumes = []

    def set_ua(self, ua):
        self._data['user_agent'] = ua

    def set_error(self, e, rc: int = 1):
        self._data['return_code'] = rc
        self._data['error'] = e

    def start(self):
        self._start_time = datetime.now()
        self._data['delta'] = str(self._start_time - self._init_time)

    def set_cookies(self, cookies):
        self._data['cookies'] = cookies

    def set_volumes(self, volumes: list):
        self._data['volumes'] = volumes

    def get(self):
        self._data['end'] = self._dt(datetime.now())
        return self._data
