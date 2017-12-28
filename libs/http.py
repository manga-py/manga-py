import requests
from urllib.parse import urlparse
from os import path
from libs.fs import get_temp_path, make_dirs, remove_file_query_params


class Http:

    allow_webp = False
    referrer_url = ""
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
    proxies = {}
    site_cookies = {}

    count_retries = 20

    skip_volumes = 0
    max_volumes = 0
    reverse_volumes = False

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

    def __safe_downloader_url_helper(self, url: str) -> str:
        if url.find('//') == 0:
            _ = urlparse(self.referrer_url).scheme if self.referrer_url else 'http'
            return _ + ':' + url
        if url.find('://') < 1:
            _ = self.referrer_url[:self.referrer_url.rfind('/')]
            if url.find('/') == 0:
                _ = urlparse(self.referrer_url)
                _ = '{}://{}'.format(_.scheme, _.netloc)
            return _.rstrip('/') + '/' + url.lstrip('/')
        return url

    def __requests_helper(
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
            location = self.__safe_downloader_url_helper(r.headers['location'])
            return self.__requests_helper(
                method, location, headers, cookies, data,
                files, max_redirects-1, timeout=timeout
            )
        return r

    def __requests(
            self, url: str, headers: dict=None, cookies: dict=None,
            data=None, method='get', files=None, timeout=None
    ) -> requests.Response:
        if not headers:
            headers = {}
        if not cookies:
            cookies = self.site_cookies
        headers.setdefault('User-Agent', self.user_agent)
        headers.setdefault('Referer', self.referrer_url)
        if self.allow_webp:
            headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        return self.__requests_helper(
            method=method, url=url, headers=headers, cookies=cookies,
            data=data, files=files, timeout=timeout, proxies=self.proxies
        )

    def get(self, url: str, headers: dict = None, cookies: dict = None) -> str:
        with self.__requests(url=url, headers=headers, cookies=cookies, method='get') as response:
            ret = response.text
            response.close()
            return ret

    def post(self, url: str, headers: dict = None, cookies: dict = None, data: dict = (), files=None) -> str:
        with self.__requests(url=url, headers=headers, cookies=cookies,
                             method='post', data=data, files=files) as response:
            text = response.text
            response.close()
            return text

    def safe_downloader(self, url, file_name, method='get') -> bool:
        try:
            make_dirs(path.dirname(file_name))
            url = self.__safe_downloader_url_helper(url)
            with open(file_name, 'wb') as out_file:
                with self.__requests(url, method=method, timeout=60) as response:
                    out_file.write(response.content)
                    response.close()
                    out_file.close()
                    return True
        except OSError:
            return False

    def prepare_cookies(self, url: str, cookies=None):
        """
        :param url:
        :param cookies: ('User-agent', {"name": "Cookie name", "value": "Cookie value",
         "domain": "Cookie domain", "path": "Cookie path") -> tuple
        :return:
        """
        session = requests.Session()
        h = session.head(url)
        if cookies:
            _ = urlparse(self.referrer_url)
            domain = "{}://{}".format(_.scheme, _.netloc)
            for i in cookies:
                if isinstance(i, str):
                    self.user_agent = i
                elif isinstance(i, dict):
                    h.cookies.set(i.get('name'), i.get('value'),
                                  domain=i.get('domain', domain), path=i.get('path', '/'))
        session.close()
        return h.cookies

    def set_proxy(self, proxy):
        self.proxies = {}
        if isinstance(proxy, dict) and hasattr(proxy, 'http'):
            self.proxies['http'] = proxy['http']
        if isinstance(proxy, dict) and hasattr(proxy, 'https'):
            self.proxies['https'] = proxy['https']

    def _download_image_name_helper(self, temp_path, i, n) -> str:
        name = remove_file_query_params(i, False)
        basename = '{:0>3}_{}'.format(n, name)
        name_loss = name.find('?') == 0
        name_len_loss = len(name) < 4
        name_dot_loss = name.find('.') < 1
        if name_loss or name_len_loss or name_dot_loss:
            basename = '{:0>3}.png'.format(n)
        return path.join(temp_path, basename)

    def _download_one_file_helper(self, url, dst, callback: callable = None):
        r = 0
        while r < self.count_retries:
            if self.safe_downloader(url, dst):
                return True

            r += 1
            mode = 'Retry'
            if r >= self.count_retries:
                mode = 'Skip image'
            if callback:
                callback(text=mode)
        return False

    def download_one_file(self, url: str, dst: str = None) -> bool:
        if not dst:
            name = path.basename(remove_file_query_params(url))
            dst = path.join(get_temp_path(), name)
        return self._download_one_file_helper(url, dst)
