from manga_py.provider import Provider
from .helpers.std import Std


class Manhwa18Net(Provider, Std):

    def get_chapter_index(self) -> str:
        chapter = self.re.search(r'-chapter-(\d+(?:\.\d+)?)', self.chapter)
        return chapter.group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}/manga-{}.html')

    def get_manga_name(self) -> str:
        return self._get_name(r'/manga-(.+)\.html')

    def get_chapters(self) -> list:
        return self._elements('a.chapter')

    def get_files(self) -> list:
        content = self.http_get(self.chapter)
        parser = self.document_fromstring(content)
        return self._images_helper(parser, '.chapter-img', 'data-original', 'src')


main = Manhwa18Net
