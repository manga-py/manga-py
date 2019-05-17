from datetime import datetime
from sys import argv

from manga_py import meta


class InfoGlobal(object):
    __slots__ = ('_store',)
    _start_time = datetime.now()

    OK = 1
    ERROR = 0

    def __init__(self):
        self._store = {
            'version': meta.__version__,
            'downloader': meta.__download_uri__,
            'delta': None,
            'start': None,
            'end': None,
            'args_raw': ' '.join(argv),
            'info': [],
        }

    @classmethod
    def _dt(cls, dt: datetime, fmt: str = '%A, %d. %B %Y %H:%M:%S'):
        return dt.strftime(fmt)

    def add_info(self, info, status=OK, message='Success'):
        self._store['info'].append({
            'data': info,
            'status': status,
            'message': message,
        })

    def get(self):
        self._store['delta'] = str(datetime.now() - self._start_time)
        self._store['start'] = self._dt(self._start_time)
        self._store['end'] = self._dt(datetime.now())
        return self._store
