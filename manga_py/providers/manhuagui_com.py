import random

from manga_py.crypt import ManhuaGuiComCrypt
from manga_py.provider import Provider
from .helpers.std import Std


class ManhuaGuiCom(Provider, Std):
    servers = [
        'i.hamreus.com:8080',
        'us.hamreus.com:8080',
        'dx.hamreus.com:8080',
        'eu.hamreus.com:8080',
        'lt.hamreus.com:8080',
    ]

    def _get_ch_idx(self):
        chapter = self.chapter
        return self.re.search(r'/comic/[^/]+/(\d+)', chapter.get('href')).group(1)

    def get_archive_name(self) -> str:
        return super().get_archive_name() + '-' + self._get_ch_idx()

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        span = chapter.cssselect('span')
        idx = self._get_ch_idx()
        if span:
            span = span[0].text_content()
            i = self.re.search(r'(\d+)', span).group(1)
            return '{}-{}'.format(i, idx)
        return '0-{}'.format(idx)

    def get_content(self):
        _ = self._get_name(r'/comic/(\d+)')
        return self.http_get('{}/comic/{}/'.format(self.domain, _))

    def get_manga_name(self) -> str:
        url = self.get_url()
        selector = 'h1'
        if self.re.search(r'/comic/\d+/\d+\.html', url):
            selector = 'h1 > a'
        return self.html_fromstring(url, selector, 0).text_content()

    def get_chapters(self):
        parser = self.document_fromstring(self.content)
        chapters = parser.cssselect('.chapter-list li > a')
        if not len(chapters):
            code = parser.cssselect('#__VIEWSTATE')[0].get('value')
            manhuagui = ManhuaGuiComCrypt()
            js = manhuagui.decrypt('LZString.decompressFromBase64("' + code + '")', '<a></a>')
            chapters = self.document_fromstring(js, '.chapter-list li > a')
        return chapters

    def parse_files_data(self, data):
        images = []
        md5 = data.get('sl', {}).get('md5', '')
        cid = data.get('cid', '')
        for i in data.get('files', []):
            prior = 3
            ln = len(self.servers)
            server = int(random.random() * (ln + prior))
            server = 0 if server < prior else server - prior
            images.append('http://{}{}{}?cid={}&md5={}'.format(
                self.servers[server],
                data.get('path', ''),
                i, cid, md5
            ))
        return images

    def get_files(self):
        url = self.chapter
        self._storage['referer'] = url
        content = self.http_get(url)
        js = self.re.search(r'\](\(function\(.+\))\s?<', content)
        if not js:
            return []
        manhuagui = ManhuaGuiComCrypt()
        data = manhuagui.decrypt(js.group(1), '')
        data = self.re.search(r'\(({.+})\)', data)
        if not data:
            return []
        data = self.json.loads(data.group(1))
        return self.parse_files_data(data)

    def get_cover(self):
        return self._cover_from_content('.hcover img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ManhuaGuiCom
