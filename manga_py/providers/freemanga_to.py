from manga_py.provider import Provider
from .helpers.std import Std


class FreeMangaTo(Provider, Std):

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'[Cc]hapter\s(\d+(?:\.\d+)?)')
        chapter = re.search(self.chapter[0]).group(1)
        return chapter.replace('.', '-')

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/(?:manga|chapter)/([^/]+)')

    def get_chapters(self):
        items = self._elements('.readIcon a')
        n = self.http().normalize_uri
        return [(i.text_content(), n(i.get('href'))) for i in items]

    def get_files(self):
        content = self.http_get(self.chapter[1])
        images = self.re.search(r'image:\s*(\[.+\])', content)
        return self.json.loads(images.group(1))

    def get_cover(self) -> str:
        return self._cover_from_content('.tooltips > img')

    def book_meta(self) -> dict:
        pass

    def chapter_for_json(self) -> str:
        return self.chapter[1]


main = FreeMangaTo
