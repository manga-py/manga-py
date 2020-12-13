from manga_py.provider import Provider
from .helpers.std import Std


class MyReadingMangaInfo(Provider, Std):

    def get_chapter_index(self, no_increment=False) -> str:
        return str(self.chapter_id)

    def get_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/([^/]+)')

    def get_chapters(self):
        v = [self.get_url()]  # current chapter
        parser = self._elements('.pagination > a')
        if not parser:
            parser = self._elements('.entry-content p > a')
        v += parser
        return v[::-1]

    def prepare_cookies(self):
        self.cf_scrape(self.get_url())

    def get_files(self):
        selector = '.entry-content div img,.entry-content p img'
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, selector)

    def get_cover(self):
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MyReadingMangaInfo
