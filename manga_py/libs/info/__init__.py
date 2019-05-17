from datetime import datetime
from sys import argv

from manga_py import meta


class Info(object):
    __slots__ = ('_store',)
    _start_time = datetime.now()

    def __init__(self, args: dict):
        self._store = {
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
        self._store['delta'] = str(datetime.now() - self._start_time)
        self._store['start'] = self._dt(self._start_time)
        self._store['end'] = self._dt(datetime.now())
        return self._store

