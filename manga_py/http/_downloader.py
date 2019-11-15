from urllib3 import HTTPResponse
from multiprocessing import cpu_count, Pool, Process
from typing import ClassVar, Optional, Union, List, Tuple, Callable, NamedTuple, Dict
from pathlib import Path
from manga_py.util.fs import is_writable
from urllib.parse import urlparse


class Task(NamedTuple):
    callback: Callable
    args: Tuple
    kwargs: Dict


class Downloader:
    cpu_count = ClassVar[int]
    tasks = ClassVar[List[Task]]

    def __init__(self):
        self.cpu_count = max(min(cpu_count(), 1), 8)
        self.tasks = []

    @staticmethod
    def url2name(url: Union[str, HTTPResponse], prefix: str = '', postfix: str = ''):
        if isinstance(url, HTTPResponse):
            url = url.geturl()
        path = urlparse(url).path  # type: str
        return '%s%s%s' % (prefix, path[path.rfind('/') + 1:], postfix)

    @staticmethod
    def download(response: HTTPResponse, location: Path):
        assert location.is_dir()
        is_writable(location)
        with open(str(location), 'wb') as w:
            w.write(response.data)

    def run(self):
        pool = Pool(self.cpu_count)
        for task in self.tasks:
            pool.apply(*task)

    def add_task(self, callback: Callable, *args, **kwargs):
        self.tasks.append(
            Task(callback=callback, args=args, kwargs=kwargs)
        )
