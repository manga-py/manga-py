from manga_py.provider import Provider
from .helpers.std import Std


class LeviatanScansCom(Provider, Std):

    def get_chapter_index(self) -> str:
        return self.re.search(r'.+/(\d+/\d+)', self.chapter).group(1).replace('/', '-')

    def get_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self.text_content(self.content, '.text-highlight')

    def get_chapters(self):
        return self._elements('.list a.item-author')

    def get_files(self):
        content = self.http_get(self.chapter)
        images = self.re.search(r'chapterPages\s*=\s*(\[.+?\])', content).group(1)
        return self.json.loads(images)

    def get_cover(self) -> str:
        image = self._elements('.media-comic-card .media-content')[0]
        return self.parse_background(image)


main = LeviatanScansCom
