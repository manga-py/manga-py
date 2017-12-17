import requests
from requests.exceptions import TooManyRedirects
from urllib.parse import urlparse
from os import path, makedirs
from libs.fs import get_temp_path
from libs.image import Image


class Http:

    allow_webp = False
    referrer_url = ""
    user_agent = ""
    proxies = {}
    site_cookies = {}

    count_retries = 20
    destination_directory = ''

    skip_volumes = 0
    max_volumes = 0
    reverse_volumes = False

    def __set_param(self, name, value):
        if value is not None:
            setattr(self, name, value)

    def __init__(
            self,
            allow_webp=None,
            referrer_url=None,
            user_agent=None,
            proxies=None,
            site_cookies=None,
            destination_directory=None,
            force_png=False,
            crop_manual=None,
            crop_image=None,
    ):
        self.main_content = ''
        self.force_png = force_png
        if crop_manual:
            self.crop_manual = crop_manual
        if crop_image:
            self.crop_image = crop_image

        self.__set_param('allow_webp', allow_webp)
        self.__set_param('referrer_url', referrer_url)
        self.__set_param('user_agent', user_agent)
        self.__set_param('proxies', proxies)
        self.__set_param('site_cookies', site_cookies)
        self.__set_param('destination_directory', destination_directory)

    @staticmethod
    def remove_file_name_params(name, save_path: bool = True) -> str:
        file_path = path.dirname(name)
        name = path.basename(name)
        if name.find('?') > 0:
            name = name[0:name.find('?')]
        return path.join(file_path, name) if save_path else name

    def __safe_downloader_url_helper(self, url: str) -> str:
        if url.find('//') == 0:
            _ = urlparse(self.referrer_url).scheme if self.referrer_url else 'http'
            return _ + ':' + url
        if url.find('://') < 1:
            _ = self.referrer_url[0:self.referrer_url.rfind('/')]
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
                raise TooManyRedirects('Too many redirects', response=r)
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
        response = self.__requests(url=url, headers=headers, cookies=cookies, method='get')
        ret = response.text
        response.close()
        return ret

    def post(self, url: str, headers: dict = None, cookies: dict = None, data: dict = (), files=None) -> str:
        response = self.__requests(url=url, headers=headers, cookies=cookies, method='post', data=data, files=files)
        text = response.text
        response.close()
        return text

    def safe_downloader(self, url, file_name, method='get') -> bool:
        try:
            url = self.__safe_downloader_url_helper(url)
            response = self.__requests(url, method=method, timeout=60)

            with open(file_name, 'wb') as out_file:
                out_file.write(response.content)
            response.close()
            return True
        except OSError:
            return False

    def prepare_cookies(self, url: str, cookies=None):
        session = requests.Session()
        h = session.head(url)
        if cookies:
            for i in cookies:
                if isinstance(i, str):
                    self.user_agent = i
                else:
                    h.cookies.set(i['name'], i['value'], domain=i['domain'], path=i['path'])
        session.close()
        return h.cookies

    def set_allow_webp(self, allow=True):
        self.allow_webp = allow

    def set_referrer_url(self, uri):
        self.referrer_url = uri

    def set_user_agent(self, agent):
        self.user_agent = agent

    def set_proxy(self, proxy):
        self.proxies = {}
        if hasattr(proxy, 'http'):
            self.proxies['http'] = proxy['http']
        if hasattr(proxy, 'https'):
            self.proxies['https'] = proxy['https']

    @staticmethod
    def _download_image_name_helper(temp_path, i, n) -> str:
        name = Http.remove_file_name_params(i, False)
        basename = '{:0>3}_{}'.format(n, name)
        name_question = name.find('?') == 0
        name_len = len(name) < 4
        name_dot = name.find('.') < 1
        if name_question or name_len or name_dot:
            basename = '{:0>3}.png'.format(n)
        return path.join(temp_path, basename)

    def __download_one_file_helper(self, url, dest, callback: callable = None):
        r = 0
        while r < self.count_retries:
            if self.safe_downloader(url, dest):
                return True
            mode = 'Skip image'
            if r < self.count_retries:
                mode = 'Retry'
            if callback:
                callback(text=mode)
        return False

    def _force_png(self, path):
        if self.force_png:
            Image.convert(path, path)

    def _crop_manual(self, path):
        if self.crop_manual:
            Image.crop_manual(path, path)

    def _crop_image(self, path):
        if self.crop_image:
            Image.crop_auto(path, path)

    def download_one_file(self, url: str, dest: str = None) -> bool:
        if not dest:
            name = path.basename(self.remove_file_name_params(url))
            dest = path.join(get_temp_path(), name)
        return self.__download_one_file_helper(url, dest)

    def __download_archive(self, url: str):
        archive_name = path.basename(url)
        if archive_name.find('.zip') > 0:
            archive_name = archive_name[:archive_name.find('.zip')]  # remove .zip
        if archive_name.find('.rar') > 0:
            archive_name = archive_name[:archive_name.find('.rar')]  # remove .rar
        dst = self._get_archive_destination(archive_name)
        self.download_one_file(url, dst)

    def _prepare_download_helper(self, items):
        if self.reverse_volumes:
            items.reverse()
        if self.skip_volumes > 0:
            items = items[self.skip_volumes:]
        if self.max_volumes > 0:
            items = items[:self.max_volumes]

        return items

    def _archive_helper(self, archives: list):
        n = 0
        for a in self._prepare_download_helper(archives):
            self.__download_archive(a)
            n += 1
        return n

    def _download_zip_only(self, volumes: list):
        if len(volumes):
            for v in volumes:
                archive = self.provider.get_zip(
                    volume=v, main_content=self.main_content,
                    get=self._get, post=self._post
                )
                self._archive_helper(archive)
            return
        archive = self.provider.get_zip(main_content=self.main_content, get=self._get, post=self._post)
        self._archive_helper(archive)

    def one_thread_downloader(self, temp_path, image, n, callback: callable = None, callback_params=None):
        image_full_name = self._download_image_name_helper(temp_path, image, n)
        result = 0
        if self.download_one_file(image, image_full_name):
            self._crop_manual(image_full_name)
            self._crop_image(image_full_name)
            self._force_png(image_full_name)
            result = 1

        callback and callback(image_full_name, callback_params)
        return result

    def _get_archive_destination(self, archive_name: str):
        if archive_name.find('?') > 0:
            archive_name = archive_name[0:archive_name.find('?')]
        d = path.join(self._get_destination_directory(), archive_name + '.zip')
        directory = path.dirname(d)
        path.isdir(directory) or makedirs(directory)
        return d

    def set_destination_directory(self, _path):
        self.destination_directory = _path

    def _get_destination_directory(self):
        return self.destination_directory
