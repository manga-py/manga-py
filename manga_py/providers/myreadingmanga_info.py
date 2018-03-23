from manga_py.provider import Provider
from .helpers.std import Std


class MyReadingMangaInfo(Provider, Std):
    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return 'vol_{:0>3}'.format(idx)

    def get_chapter_index(self, no_increment=False) -> str:
        return str(self.chapter_id)

    def get_main_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.info/([^/]+)')

    def get_chapters(self):
        v = [self.get_url()]  # current chapter
        parser = self._elements('.pagination > a')
        if not parser:
            parser = self._elements('.entry-content p > a')
        v += parser
        return v[::-1]

    def prepare_cookies(self):
        self.cf_protect(self.get_url())

    def get_files(self):
        selector = '.entry-content div img,.entry-content p img'
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, selector)

    def get_cover(self):
        pass


main = MyReadingMangaInfo
