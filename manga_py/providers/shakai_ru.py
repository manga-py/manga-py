from manga_py.provider import Provider
from .helpers.std import Std


class ShakaiRu(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-', 2)
        return 'vol_{:0>3}-{}'.format(*self._idx_to_x2(idx))

    def get_chapter_index(self) -> str:
        idx = self.chapter.get('data-first')
        return idx.replace('_', '-')

    def get_main_content(self):
        idx = self._get_name(r'/manga[^/]*/(\d+)')
        _ = {
            'dataRun': 'api-manga',
            'dataRequest': idx
        }
        page_content = str(self.http_post('http://shakai.ru/take/api-manga/request/shakai', data=_))
        return self.json.loads(page_content)

    def get_manga_name(self) -> str:
        parser = self.content.get('post', [])
        idx = self._get_name(r'/manga[^/]*/(\d+)')
        parser = parser[3] if len(parser) > 3 else idx
        return parser.split('/')[0].strip()

    def get_chapters(self):
        return self.content.get('data', [])[::-1]

    def get_files(self):
        chapter = self.chapter
        if isinstance(chapter, dict):
            return chapter.get('data-second', [])
        return []

    def get_cover(self):
        pass  # FIXME HOME


main = ShakaiRu
