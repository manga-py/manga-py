import requests
from urllib.parse import urlparse
from os import path
from libs.fs import get_temp_path, make_dirs, remove_file_query_params


class UrlNormalizer:

    @staticmethod
    def __relative_scheme(uri, ref):
        scheme = urlparse(ref).scheme if ref else 'http'
        return scheme + ':' + uri

    @staticmethod
    def __get_domain(uri, ref):
        new_url = ref[:ref.rfind('/')]
        if uri.find('/') == 0:
            new_url = urlparse(ref)
            new_url = '{}://{}'.format(new_url.scheme, new_url.netloc)
        return new_url

    @staticmethod
    def url_helper(url: str, base_url: str) -> str:
        if url.find('//') == 0:  # abs without scheme
            return UrlNormalizer.__relative_scheme(url, base_url)
        if url.find('://') < 1:  # relative
            _ = UrlNormalizer.__get_domain(url, base_url)
            return '%s/%s' % (_.rstrip('/'), url.lstrip('/'))
        return url

    @staticmethod
    def image_name_helper(temp_path, i, n) -> str:
        name = remove_file_query_params(i, False)
        basename = '{:0>3}_{}'.format(n, name)
        name_loss = name.find('?') == 0
        name_len_loss = len(name) < 4
        name_dot_loss = name.find('.') < 1
        if name_loss or name_len_loss or name_dot_loss:
            basename = '{:0>3}.png'.format(n)
        return path.join(temp_path, basename)


class Request:
    referrer_url = ''
    proxies = {}
    allow_webp = False
    user_agent = '%s %s %s %s' % (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'AppleWebKit/537.36 (KHTML, like Gecko)',
        'Chrome/60.0.3112.101',
        'Safari/537.36'
    )
    cookies = {}

    def _get_cookies(self, cookies = None):
        return cookies if cookies else self.cookies

    def _requests_helper(
            self, method, url, headers=None, cookies=None, data=None,
            files=None, max_redirects=10, timeout=None, proxies=None
    ) -> requests.Response:
        r = getattr(requests, method)(
            url=url, headers=headers, cookies=cookies, data=data,
            files=files, allow_redirects=False, proxies=proxies
        )
        if r.is_redirect:
            if max_redirects < 1:
                raise AttributeError('Too many redirects')
            location = UrlNormalizer.url_helper(r.headers['location'], self.referrer_url)
            return self._requests_helper(
                method, location, headers, cookies, data,
                files, max_redirects-1, timeout=timeout
            )
        return r

    def _requests(
            self, url: str, headers: dict=None, cookies: dict=None,
            data=None, method='get', files=None, timeout=None
    ) -> requests.Response:
        if not headers:
            headers = {}
        cookies = self._get_cookies(cookies)
        headers.setdefault('User-Agent', self.user_agent)
        headers.setdefault('Referer', self.referrer_url)
        if self.allow_webp:
            headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=1.0,image/webp,image/apng,*/*;q=1.0'
        return self._requests_helper(
            method=method, url=url, headers=headers, cookies=cookies,
            data=data, files=files, timeout=timeout, proxies=self.proxies
        )

    def get(self, url: str, headers: dict = None, cookies: dict = None) -> str:
        with self._requests(
                url=url,
                headers=headers,
                cookies=cookies,
                method='get'
        ) as response:
            ret = response.text
            response.close()
            return ret

    def post(self, url: str, headers: dict = None, cookies: dict = None, data: dict = (), files=None) -> str:
        with self._requests(
                url=url,
                headers=headers,
                cookies=cookies,
                method='post',
                data=data,
                files=files
        ) as response:
            text = response.text
            response.close()
            return text

    def reset_proxy(self):
        self.proxies = {}

    def set_proxy(self, proxy):
        self.reset_proxy()
        if isinstance(proxy, dict):
            self.proxies['http'] = proxy.get('http', None)
            self.proxies['https'] = proxy.get('https', None)
        elif isinstance(proxy, str):
            self.proxies['http'] = proxy

    def __parse_cookies(self, response: requests.Response, domain: str, cookies: dict):
            for i in cookies:
                if isinstance(i, str):
                    self.user_agent = i
                elif isinstance(i, dict):
                    response.cookies.set(
                        name=i.get('name'),
                        value=i.get('value'),
                        domain=i.get('domain', domain),
                        path=i.get('path', '/')
                    )

    def get_base_cookies(self, url: str, cookies=None):
        """
        :param url:
        :param cookies: ('User-agent', {"name": "Cookie name", "value": "Cookie value",
         "domain": "Cookie domain", "path": "Cookie path") -> tuple
        :return:
        """
        session = requests.Session()
        h = session.head(url)
        if isinstance(cookies, dict):
            _ = urlparse(self.referrer_url)
            domain = "{}://{}".format(_.scheme, _.netloc)
            self.__parse_cookies(h, domain, cookies)
        session.close()
        return h.cookies


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
            make_dirs(path.dirname(file_name))
            url = UrlNormalizer.url_helper(url, self.referrer_url)
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
            name = path.basename(remove_file_query_params(url))
            dst = path.join(get_temp_path(), name)
        return self._download_one_file_helper(url, dst)


class ChaptersDownloader:
    def __init__(
            self,
            allow_webp: bool = None,
            referrer_url: str = None,
            user_agent: str = None,
            site_cookies: dict = None,
            skip_chapters=None,
            proxies=None,
    ):
        pass
