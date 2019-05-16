from datetime import datetime
from copy import deepcopy
from sys import argv
try:
    from manga_py import meta
except ImportError:
    pass


class Info:
    _data = None
    _start_time = None

    def __init__(self, args: dict):
        self._start_time = datetime.now()
        self._data = {
            'site': args.get('url'),
            'downloader': meta.__download_uri__,
            'version': meta.__version__,
            'delta': None,
            'start': None,
            'end': None,
            'user_agent': None,
            'cookies': None,
            'args': args,
            'args_raw': ' '.join(argv),
            'return_code': 0,
            'error': None,
            'chapters': [],
        }

    @classmethod
    def _dt(cls, dt: datetime, fmt: str = '%A, %d. %B %Y %H:%M:%S'):
        return dt.strftime(fmt)

    def get(self):
        self._data['delta'] = str(datetime.now() - self._start_time)
        self._data['start'] = self._dt(self._start_time)
        self._data['end'] = self._dt(datetime.now())
        return self._data

