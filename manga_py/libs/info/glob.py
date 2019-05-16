from datetime import datetime
from copy import deepcopy
from sys import argv
try:
    from manga_py import meta
except ImportError:
    pass


class InfoGlobal:
    OK = 1
    ERROR = 0
    _data = None

    def __init__(self):
        self._start_time = datetime.now()
        self._data = {
            'version': meta.__version__,
            'license': meta.__license__,
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
        self._data['info'].append({
            'data': info,
            'status': status,
            'message': message,
        })

    def get(self):
        self._data['delta'] = str(datetime.now() - self._start_time)
        self._data['start'] = self._dt(self._start_time)
        self._data['end'] = self._dt(datetime.now())
        return deepcopy(self._data)
