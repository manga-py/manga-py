from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from concurrent.futures.process import ProcessPoolExecutor
from typing import List, Callable, Optional
from manga_py.libs.provider.file_tuple import FileTuple
from manga_py.libs.log import logger
# https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247(v=vs.85).aspx


class Threading:
    __slots__ = ('_max_threads', '_items', '_target', '_each_file_callback', '_final', '_success')

    def __init__(self):
        self._items = []
        self._target = None
        self._each_file_callback = None
        self._final = None
        self._success = True
        try:
            import multiprocessing
            self._max_threads = multiprocessing.cpu_count()
        except ImportError:
            self._max_threads = 2

    def __default_final(self, *args, **kwargs): pass

    def set_callbacks(
            self,
            target: Callable[[FileTuple, Callable], None],
            each_file_callback: Callable,
            final_callback: Optional[Callable] = None,
    ):
        """
        :param target: params[file_params, after_download_callback]
        :param each_file_callback: after_download_callback
        :param final_callback:
        :return:
        """
        self._target = target
        self._each_file_callback = each_file_callback
        self._final = final_callback

    def items(self, items: List[FileTuple]):
        self._items = items

    # TODO!
    def _urls(self) -> List[FileTuple]:
        result = []
        # for i in self._items:  # type: FileTuple
            # for img in i.paths
        return

    def __prepare(self):
        self._success = True
        if self._target is None:
            raise AttributeError('Target is None')
        if self._each_file_callback is None:
            raise AttributeError('Each-file-callback is None')

    def run(self):
        log = logger()
        with ThreadPoolExecutor(max_workers=self._max_threads) as executor:  # type: ProcessPoolExecutor
            future = {executor.submit(self._target, file, self._each_file_callback): file for file in self._items}
            for idx in as_completed(future):  # type: Future
                url = future[idx]
                try:
                    data = idx.result(timeout=30)
                except Exception as exc:
                    log.warning('Error downloading')
                else:
                    print('%r page is %d bytes' % (url, len(data)))

        (self._final or self.__default_final)()

