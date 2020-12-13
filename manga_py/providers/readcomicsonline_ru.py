from manga_py.provider import Provider
from .helpers.std import Std


class ReadComicsOnlineRu(Provider, Std):
    def get_chapter_index(self, no_increment=False) -> str:
        chapter = self.re.search(r'/([\w\d_-]+)$', self.chapter).group(1)
        return chapter.replace('.', '-').replace('_', '-')

    def get_content(self):
        return self._get_content(r'{}/comic/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'/comic/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapters .chapter-title-rtl a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '#all > img', 'data-src')

    def get_cover(self):
        return self._cover_from_content('.boxed .img-responsive')


main = ReadComicsOnlineRu
