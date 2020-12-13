from manga_py.provider import Provider
from .helpers.std import Std


class MangaMexatCom(Provider, Std):

    def get_chapter_index(self) -> str:
        return self.chapter[1].replace('.', '-')

    def get_content(self):
        return self._get_content('{}/category/{}/')

    def get_manga_name(self) -> str:
        return self._get_name('/category/([^/]+)')

    def get_chapters(self):
        items = self._elements('.content .entry td + td > a')
        return [(i.get('href', i.text_content().strip())) for i in items]

    def _get_img(self, parser):
        return self._images_helper(parser, '.pic > a > img')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        pages = self._first_select_options(parser, '#manga_pid', True)
        images = self._get_img(parser)
        for p in pages:
            url = self.chapter + '?pid=' + p.get('value')
            parser = self.html_fromstring(url)
            images += self._get_img(parser)
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('.archive-meta img')

    def book_meta(self) -> dict:
        pass

    def chapter_for_json(self):
        return self.chapter[0]


main = MangaMexatCom
