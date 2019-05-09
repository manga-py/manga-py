from lxml.html import HtmlElement

from manga_py.provider import Provider
from .helpers import e_hentai_org
from .helpers.std import Std


class EHentaiOrg(Provider, Std):
    helper = None

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        _url = None
        if isinstance(url, HtmlElement):
            _url = self.helper.get_image(url)
        return super().save_file(idx=idx, callback=callback, url=_url, in_arc_name=in_arc_name)

    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_main_content(self):
        return self.http_get(self.helper.get_url())

    def get_manga_name(self) -> str:
        return self._get_name('/g/([^/]+/[^/?]+)').replace('/', '-')

    def prepare_cookies(self):
        self.helper = e_hentai_org.EHentaiOrg(self)
        self.http().cookies['nm'] = "1"  # issue #178

    def get_chapters(self):
        parser = self.document_fromstring(self.content)
        max_idx = self.helper.get_pages_count(parser)
        return list(range(max_idx, -1, -1))

    def get_files(self):
        url = self.helper.get_url() + '?p='
        select = '#gdt .gdtm > div > a'

        idx = self.chapter
        if idx == 0:
            content = self.content
        else:
            content = self.http_get('{}{}'.format(url, idx))
        return self.document_fromstring(content, select)

    def get_cover(self) -> str:
        return self._cover_from_content('#gd1 > div')

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.get_url()


main = EHentaiOrg
