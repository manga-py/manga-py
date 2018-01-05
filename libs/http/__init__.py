from libs.fs import get_temp_path, make_dirs, remove_file_query_params, basename, path_join, dirname
from .multi_threads import MultiThreads
from .request import Request
from .url_normalizer import UrlNormalizer


class Http(Request):

    count_retries = 20

    def __init__(
            self,
            allow_webp=None,
            referrer_url=None,
            user_agent=None,
            proxies=None,
            site_cookies=None,
    ):
        self.__set_param('allow_webp', allow_webp)
        self.__set_param('referrer_url', referrer_url)
        self.__set_param('user_agent', user_agent)
        self.__set_param('proxies', proxies)
        self.__set_param('site_cookies', site_cookies)

    def __set_param(self, name, value):
        if value is not None:
            _type = type(getattr(self, name))
            if not isinstance(value, _type):
                raise AttributeError('{} type not {}'.format(name, _type))
            setattr(self, name, value)

    def _safe_downloader(self, url, file_name, method='get') -> bool:
        try:
            make_dirs(dirname(file_name))
            url = self.normalize_uri(url)
            with open(file_name, 'wb') as out_file:
                with self._requests(url, method=method, timeout=60) as response:
                    out_file.write(response.content)
                    response.close()
                    out_file.close()
        except OSError:
            return False
        return True

    def _download_one_file_helper(self, url, dst, callback: callable = None):
        r = 0
        while r < self.count_retries:
            if self._safe_downloader(url, dst):
                return True

            r += 1
            mode = 'Retry'
            if r >= self.count_retries:
                mode = 'Skip image'
            callable(callback) and callback(text=mode)
        return False

    def download_file(self, url: str, dst: str = None) -> bool:
        if not dst:
            name = basename(remove_file_query_params(url))
            dst = path_join(get_temp_path(), name)
        return self._download_one_file_helper(url, dst)

    def normalize_uri(self, uri):
        return UrlNormalizer.url_helper(uri, self.referrer_url)

    def multi_download_get(self, urls, dst: str = None, callback: callable = None):
        threading = MultiThreads()
        for url in urls:
            threading.add(self.download_file, (url, dst))
        threading.start(callback)
