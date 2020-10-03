from abc import ABCMeta
from time import sleep
from urllib.parse import unquote

from requests import get

from manga_py.provider import Provider


class NineHelper(Provider, metaclass=ABCMeta):
    img_server = 'https://ta1.taadd.com'

    def allow_auto_change_url(self):
        return False

    def re_name(self, url):
        return self.re.search(r'/manga/(.+)\.html', url)

    @staticmethod
    def normalize_name(name, normalize):
        if normalize:
            name = unquote(name)
        return name

    def parse_img_uri(self, url):
        return self.re.search('://[^/]+/(.+)', url).group(1)

    def get_img_server(self, content):
        server = self.re.search(r'img_url\s?=\s?"([^"]+)', content)
        if server:
            return server.group(1)
        return self.img_server

    def get_files_on_page(self, content):
        result = self.document_fromstring(content, 'em a.pic_download')
        if not result:
            return []
        images = []
        pic_url = self.get_img_server(content)
        for i in result:
            src = self.parse_img_uri(i.get('href'))
            images.append('{}/{}'.format(pic_url, src))
        return images

    def _get_page_content(self, url):
        sleep(.6)
        return get(
            url,
            headers={
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'Referer': '',
            }  # fix guard
        ).text

    def prepare_cookies(self):
        self._storage['cookies'].setdefault('__cfduid', '1a2b3c4d5e')
