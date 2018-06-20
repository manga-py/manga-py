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
        'error': False,
        'error_msg': '',
        'volumes': [
            {
              'name': 'Kumo desu ga, nani ka? - 0',
              'path': 'Manga/kumo-desu-ga-nani-ka/vol_000.zip',
            },
            {
              'name': 'Kumo desu ga, nani ka? - 1',
              'path': 'Manga/kumo-desu-ga-nani-ka/vol_001.zip',
            },
        ],
    }
    """
    _data = None
    _start_time = None

    @staticmethod
    def _dt(dt, fmt: str = '%A, %d. %B %Y %H:%M:%S'):
        return dt.strftime(fmt)

    def __init__(self, args: Namespace):  # see manga_py.cli arguments
        _args = args.__dict__
        _args['_raw_params'] = ' '.join(argv)
        self._data = {
            'site': args.url,
            'downloader': meta.__downloader_uri__,
            'version': meta.__version__,
            'delta': None,
            'init': self._dt(datetime.now()),
            'start': None,
            'end': None,
            'user_agent': None,
            'cookies': None,
            'args': _args,
            'return_code': 0,
            'error': False,
            'error_msg': None,
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

    def set_cookies(self, cookies):
        self._data['cookies'] = cookies

    def set_volumes(self, volumes: list):
        self._data['volumes'] = volumes

    def set_last_volume_error(self, error_message):
        try:
            self._data['volumes'][-1]['error'] = True
            self._data['volumes'][-1]['error_message'] = error_message
        except IndexError:
            pass

    def add_volume(self, url: str, path: str, files: list = None):
        volume = {
            'url': url,
            'path': path,
            'error': False,
            'error_message': '',
        }

        if files is not None:
            volume['files'] = files
            volume['num_files'] = len(files)

        self._data['volumes'].append(volume)

    def get(self):
        self._data['delta'] = str(datetime.now() - self._start_time)
        self._data['start'] = self._dt(self._start_time)
        self._data['end'] = self._dt(datetime.now())
        return self._data
