from datetime import datetime
from sys import argv
try:
    from manga_py import meta
except ImportError:
    pass


class Info:
    _provider = None
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

    def set_ua(self, ua):
        self._data['user_agent'] = ua

    def set_error(self, error):
        self._data['error'] = error

    def set_cookies(self, cookies):
        self._data['cookies'] = cookies

    def set_chapters(self, chapters):
        self._data['chapters'] = chapters

    def get(self):
        self._data['delta'] = str(datetime.now() - self._start_time)
        self._data['start'] = self._dt(self._start_time)
        self._data['end'] = self._dt(datetime.now())
        return self._data


class InfoGlobal:
    OK = 1
    ERROR = 0
    _data = None

    def __init__(self):
        self._start_time = datetime.now()
        self._data = {
            'version': meta.__version__,
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
        return self._data
