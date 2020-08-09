from sys import stderr
from time import sleep
import requests
from logging import warning, error, info

from manga_py.fs import get_temp_path, make_dirs, remove_file_query_params, basename, path_join, dirname, file_size
from .multi_threads import MultiThreads
from .request import Request
from .url_normalizer import normalize_uri


class Http(Request):
    count_retries = 20
    has_error = False
    mute = False

    def __init__(
            self,
            allow_webp=True,
            referer='',
            user_agent=None,
            proxies=None,
            cookies=None,
            kwargs=None
    ):
        super().__init__()
        self.__set_param('allow_webp', allow_webp)
        self.__set_param('referer', referer)
        self.__set_param('user_agent', user_agent)
        self.__set_param('proxies', proxies)
        self.__set_param('cookies', cookies)
        self.__set_param('kwargs', kwargs)

    def __set_param(self, name, value):
        if value is not None:
            self_val = getattr(self, name)
            _type = type(self_val)
            if self_val is not None and not isinstance(value, _type):
                raise AttributeError('{} type not {}'.format(name, _type))
            setattr(self, name, value)

    def _download(self, file_name, url, method):
        now_try_count = 0
        with open(file_name, 'wb') as out_file:
            now_try_count += 1
            response = self.requests(url, method=method, timeout=60, allow_redirects=True)
            if response.status_code >= 400:
                error('\nERROR! Code {}\nUrl: {}\n'.format(
                    response.status_code,
                    url,
                ))
                sleep(2)
                if response.status_code == 403:
                    response = requests.request(method=method, url=url, timeout=60, allow_redirects=True)

            if response.status_code < 400:
                out_file.write(response.content)

            response.close()
            out_file.close()

    def _safe_downloader(self, url, file_name, method='get') -> bool:
        try:
            make_dirs(dirname(file_name))
            url = self.normalize_uri(url)
            self._download(file_name, url, method)
        except OSError as ex:
            error(ex)
            return False
        return True

    def _download_one_file_helper(self, url, dst, callback: callable = None, success_callback: callable = None,
                                  callback_args=()):
        r = 0
        while r < self.count_retries:
            if self._safe_downloader(url, dst):
                if file_size(dst) < 64:
                    return None
                callable(success_callback) and success_callback(dst, *callback_args)
                return True

            r += 1
            mode = 'Retry'
            if r >= self.count_retries:
                mode = 'Skip image'
                warning('%s: %s' % (mode, url))
            callable(callback) and callback(text=mode)
        return False

    def download_file(self, url: str,
                      dst: str = None,
                      idx=-1,
                      callback: callable = None,
                      success_callback: callable = None,
                      callback_args=()) -> bool:
        if not dst:
            name = basename(remove_file_query_params(url))
            dst = path_join(get_temp_path(), name)

        info('Downloading ({}): {}'.format(idx, url))

        result = self._download_one_file_helper(url, dst, callback, success_callback, callback_args)
        if result is None and not self.mute:
            self.has_error = True  # issue 161
            warning('\nWarning: 0 bit image downloaded, please check for redirection or broken content')
            if ~idx:
                warning('Broken url: %s\nPage idx: %d' % (url, (1 + idx)), file=stderr)
        return result

    def normalize_uri(self, uri, referer=None):
        if not referer:
            referer = self.referer
        if isinstance(uri, str):
            return normalize_uri(uri.strip(), referer)
        return uri

    def multi_download_get(self, urls, dst: str = None, callback: callable = None):
        threading = MultiThreads()
        for idx, url in enumerate(urls):
            threading.add(self.download_file, (url, dst, idx))
        threading.start(callback)

    def get_redirect_url(self, url, **kwargs):
        location = self.requests(url=url, method='head', **kwargs)
        url = location.headers.get('Location', url)
        return self.normalize_uri(url)
