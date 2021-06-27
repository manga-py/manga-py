from manga_py.provider import Provider
from .helpers.std import Std


class GenkanIo(Provider, Std):
    def get_chapter_index(self) -> str:
        return self.chapter[1]

    def get_content(self):
        return self.http_get(self.re.search(
            r'(https?://.+?/manga/[^/]+)',
            self.get_url()
        ).group(1))

    def get_manga_name(self) -> str:
        parser = self.document_fromstring(self.content, 'h2', 0)
        return self.element_text_content_full(parser)

    def get_chapters(self):
        return [(el.get('href'), self.element_text_content_full(el)) for el in self._elements('section table td:nth-child(1) > a')]

    def get_files(self):
        parser = self.html_fromstring(self.chapter[0])
        return self._images_helper(parser, '.container > img')

    def get_cover(self) -> str:
        return self._cover_from_content('section > div > img')

    def prepare_cookies(self):
        self.http().referer = self.domain
        self.http().allow_send_referer = True

    def chapter_for_json(self) -> str:
        return self.chapter[0]


main = GenkanIo
