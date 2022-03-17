from manga_py.provider import Provider
from .helpers.std import Std


class MangaOwlNet(Provider, Std):
    def get_archive_name(self) -> str:
        return self.chapter[1]

    def get_chapter_index(self) -> str:
        return self.chapter[1]

    def get_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self.text_content(self.content, '.single_detail h2')

    def get_chapters(self):
        chapters = self.document_fromstring('a.chapter-url', self.content)
        return [
            (c.get('data-href'), c.cssselect('label.chapter-title'), ) for c in chapters
        ]

    def get_files(self):
        parser = self.document_fromstring(self.http_get(self.chapter[0]))
        return self._images_helper(parser, 'img.ows-lazy', 'data-src', 'src')

    def get_cover(self) -> str:
        return self._cover_from_content('.single_detail a>img', 'data-src')

    def chapter_for_json(self) -> str:
        return self.chapter[0]


main = MangaOwlNet
