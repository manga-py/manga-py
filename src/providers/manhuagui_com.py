from src.provider import Provider
from src.crypt.manhuagui_com_crypt import ManhuaGuiComCrypt

import random


class ManhuaGuiCom(Provider):
    servers = [
        'i.hamreus.com:8080',
        'us.hamreus.com:8080',
        'dx.hamreus.com:8080',
        'eu.hamreus.com:8080',
        'lt.hamreus.com:8080',
    ]

    def _get_ch_idx(self):
        chapter = self.get_current_chapter()
        return self.re.search('/comic/[^/]+/(\\d+)', chapter.get('href')).group(1)

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return 'vol_{:0>4}-{}'.format(idx, self._get_ch_idx())

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        span = chapter.cssselect('span')
        idx = self._get_ch_idx()
        if span:
            span = span[0].text_content()
            i = self.re.search('(\\d+)', span).group(1)
            return '{}-0'.format(i, idx)
        return '0-{}'.format(idx)

    def get_main_content(self):
        _ = self.re.search('/comic/(\\d+)', self.get_url()).group(1)
        return self.http_get('{}/comic/{}/'.format(self.get_domain(), _))

    def get_manga_name(self) -> str:
        url = self.get_url()
        selector = 'h1'
        if self.re.search('/comic/\\d+/\\d+\\.html', url):
            selector = 'h1 > a'
        return self.html_fromstring(url, selector, 0).text_content()

    def get_chapters(self):
        parser = self.document_fromstring(self.get_storage_content())
        chapters = parser.cssselect('.chapter-list li > a')
        if len(chapters) < 1:
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

    def chapter_url(self):
        url = self.get_current_chapter().get('href')
        return self.http().normalize_uri(url)

    def get_files(self):
        url = self.chapter_url()
        self._storage['referer'] = url
        content = self.http_get(url)
        js = self.re.search('\\](\\(function\\(.+\\))\\s?<', content)
        if not js:
            return []
        manhuagui = ManhuaGuiComCrypt()
        data = self.re.search('cInfo=(.+)\\|\\|', manhuagui.decrypt(js.group(1), ''))
        if not data:
            return []
        data = self.json.loads(data.group(1))
        return self.parse_files_data(data)


main = ManhuaGuiCom
