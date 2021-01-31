from lxml.html import HtmlElement

from manga_py.provider import Provider
from .helpers import e_hentai_org
from .helpers.std import Std
from time import sleep


class EHentaiOrg(Provider, Std):
    helper = None

    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_content(self):
        return self.http_get(self.helper.get_url())

    def get_manga_name(self) -> str:
        return self._get_name('/g/([^/]+/[^/?]+)').replace('/', '-')

    def prepare_cookies(self):
        self.helper = e_hentai_org.EHentaiOrg(self)
        self.http().cookies['nw'] = "1"  # issue #178
        self.http().cookies['nm'] = "1"  # issue #178

    def get_chapters(self):
        parser = self.document_fromstring(self.content)
        max_idx = self.helper.get_pages_count(parser)
        self.log('Please, wait...\n')
        return list(range(max_idx, -1, -1))

    def get_files(self):
        url = self.helper.get_url() + '?p='
        selector = '#gdt div[class^=gdt] a'
        idx = self.chapter
        if idx == 0:
            content = self.content
        else:
            content = self.http_get('{}{}'.format(url, idx))
        pages = self.document_fromstring(content, selector)

        n = self.http().normalize_uri
        f = self.document_fromstring

        images = []
        for page in pages:
            _url = n(page.get('href'))
            images.append(n(f(self.http_get(_url), '#img', 0).get('src')))
            sleep(.1)
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('#gd1 > div')

    def chapter_for_json(self):
        return self.get_url()


main = EHentaiOrg
