from manga_py.provider import Provider
from .helpers.std import Std


class HentaiLxxCom(Provider, Std):
    def get_archive_name(self) -> str:
        return self.chapter[1]

    def get_chapter_index(self) -> str:
        return self.chapter[1]

    def get_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        el = self.document_fromstring(self.content, '.title-detail', 0)
        return self.element_text_content(el)

    def get_chapters(self):
        n = self.http().normalize_uri
        return [(n(e.get('href')), self.element_text_content(e)) for e in self._elements('li a.seen')]

    def get_files(self):
        parser = self.html_fromstring(self.chapter[0])
        images = self._images_helper(parser, '#content_chap > .separator > a', 'href')
        if len(images) > 0:
            return images

        return self._images_helper(parser, '#content_chap > div > img')

    def get_cover(self) -> str:
        return self._cover_from_content('#mainpage .row .text-center img[width]')

    def chapter_for_json(self) -> str:
        return self.chapter[0]


main = HentaiLxxCom
